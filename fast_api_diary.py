import json
import requests
import datetime
import time
import sys
import os

BASE_URL = "https://vtuapi.internyet.in/api/v1"

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"CRITICAL ERROR: {filepath} not found.")
        sys.exit(1)
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    print("Initializing High-Speed API Bot...")
    creds = load_json('credentials.json')
    entries = load_json('internship_diary_entries.json')

    print(f"Loaded {len(entries)} diary entries to process.")

    session = requests.Session()
    # Use standard browser headers to match normal traffic
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://vtu.internyet.in",
        "Referer": "https://vtu.internyet.in/"
    })

    # 1. Login Phase
    print("\n[1/4] Logging in via API...")
    login_resp = session.post(f"{BASE_URL}/auth/login", json={
        "email": creds['email'],
        "password": creds['password']
    })
    
    if login_resp.status_code != 200:
        print(f"CRITICAL ERROR: Login failed. HTTP {login_resp.status_code}")
        print(f"Response: {login_resp.text}")
        sys.exit(1)
        
    print("Login successful! Session cookies firmly established.")

    # 2. Fetch Internship Details Phase
    print("\n[2/4] Fetching internship identifier...")
    internships_resp = session.get(f"{BASE_URL}/student/internship-applys?page=1&status=6")
    if internships_resp.status_code != 200:
        print(f"CRITICAL ERROR: Failed to fetch internships. HTTP {internships_resp.status_code}")
        print(f"Response: {internships_resp.text}")
        sys.exit(1)
        
    try:
        data = internships_resp.json()
        # Parse nested data structure securely
        if 'data' in data and 'data' in data['data']:
            internships = data['data']['data']
        elif 'data' in data and isinstance(data['data'], list):
            internships = data['data']
        else:
            internships = data

        if not internships:
             print("CRITICAL ERROR: No active internships found for this account.")
             sys.exit(1)
             
        # Extract ID
        first_internship = internships[0]
        # In case the key is named slightly differently
        internship_id = first_internship.get('internship_id') or first_internship.get('id')
        
        if not internship_id:
             print("CRITICAL ERROR: Could not parse internship_id from the backend response.")
             print(f"Debug Info: {json.dumps(first_internship, indent=2)}")
             sys.exit(1)
             
        print(f"Successfully discovered Internship ID: {internship_id}")
    except Exception as e:
        print(f"CRITICAL ERROR parsing internship response: {e}")
        print(f"Raw text: {internships_resp.text}")
        sys.exit(1)

    # 3. Fetch Skill Mappings Phase
    print("\n[3/4] Downloading VTU master skill list...")
    skills_resp = session.get(f"{BASE_URL}/master/skills")
    if skills_resp.status_code != 200:
         print(f"CRITICAL ERROR: Failed to fetch skills. HTTP {skills_resp.status_code}")
         print(skills_resp.text)
         sys.exit(1)
         
    try:
        data = skills_resp.json()
        skills_list = data.get('data', data) if isinstance(data, dict) else data
        
        # Build strict dictionary mapping lowercase name to string ID (e.g. "java" -> "10")
        skill_map = {}
        for skill in skills_list:
            sid = str(skill.get('id', ''))
            sname = str(skill.get('name', skill.get('title', ''))).lower().strip()
            if sid and sname:
                skill_map[sname] = sid
                
        if not skill_map:
             print("CRITICAL ERROR: Skill map is empty. Could not parse skills API.")
             sys.exit(1)
             
        print(f"Successfully mapped {len(skill_map)} skills to backend IDs.")
    except Exception as e:
        print(f"CRITICAL ERROR parsing skills response: {e}")
        sys.exit(1)

    # 4. Strict Submission Loop Phase
    print("\n[4/4] Starting Strict Validation & Submission Loop...")
    
    for idx, entry in enumerate(entries):
        entry_name = f"Entry {entry.get('day', entry.get('week', idx+1))}"
        print(f"-> Processing {entry_name} for Date {entry.get('date', 'UNKNOWN')}...")
        
        # A. Date validation & Conversion (DD-MM-YYYY -> YYYY-MM-DD)
        try:
             dt = datetime.datetime.strptime(entry['date'], "%d-%m-%Y")
             formatted_date = dt.strftime("%Y-%m-%d")
        except Exception:
             print(f"   [!] CRITICAL ERROR: Date '{entry.get('date')}' is invalid. MUST be DD-MM-YYYY format.")
             print(f"   [!] Halting automation immediately to prevent corrupt submissions.")
             sys.exit(1)
             
        # B. Resolve Skills to IDs securely
        resolved_skill_ids = []
        for s in entry.get('skills_used', []):
            s_lower = s.lower().strip()
            if s_lower in skill_map:
                resolved_skill_ids.append(skill_map[s_lower])
            else:
                print(f"   [!] CRITICAL ERROR: Skill '{s}' was not found in the VTU database.")
                print(f"   [!] Halting automation immediately.")
                sys.exit(1)
                
        if not resolved_skill_ids:
             print(f"   [!] CRITICAL ERROR: No valid skills provided for {entry_name}.")
             sys.exit(1)
             
        # C. Validate data lengths and types
        summary = str(entry.get('work_summary', '')).strip()
        learnings = str(entry.get('learnings_outcomes', '')).strip()
        
        try:
             hours = float(entry.get('hours_worked', 0))
        except ValueError:
             print(f"   [!] CRITICAL ERROR: hours_worked must be a number for {entry_name}.")
             sys.exit(1)
        
        if not summary or not learnings or hours <= 0:
             print(f"   [!] CRITICAL ERROR: Missing or invalid summary, learnings, or hours for {entry_name}.")
             sys.exit(1)
             
        # D. Build Exact Payload Expected by VTU Server
        payload = {
            "internship_id": internship_id,
            "date": formatted_date,
            "description": summary,
            "hours": hours,
            "links": "",
            "blockers": "",
            "learnings": learnings,
            "mood_slider": 5, # Standard happy mood
            "skill_ids": resolved_skill_ids
        }
        
        # E. Transmit Payload
        print(f"   Submitting payload for {formatted_date}...")
        submit_resp = session.post(f"{BASE_URL}/student/internship-diaries/store", json=payload)
        
        # F. Ensure Success
        if submit_resp.status_code in [200, 201]:
             # Double check internal JSON success code if VTU returns 200 for errors
             try:
                 resp_json = submit_resp.json()
                 if resp_json.get('success') is False:
                     print(f"   [!] CRITICAL ERROR: VTU API rejected the submission with message: {resp_json.get('message')}")
                     sys.exit(1)
             except: pass
                 
             print(f"   [✓] SUCCESS: {entry_name} securely saved into VTU database!")
             time.sleep(2)  # Respect API rate limits
        else:
             print(f"   [!] CRITICAL ERROR: VTU Server returned HTTP {submit_resp.status_code}")
             print(f"   [!] Response text: {submit_resp.text}")
             print(f"   [!] Halting immediately.")
             sys.exit(1)
             
    print("\n=======================================================")
    print("ALL ENTRIES SUCCESSFULLY SUBMITTED IN RECORD TIME!")
    print("Automation Complete.")
    print("=======================================================")

if __name__ == "__main__":
    main()
