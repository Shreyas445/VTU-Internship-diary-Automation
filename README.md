# VTU Internship Diary Automation

This Python script automates the process of filling out the daily internship diary on the VTU Internship Portal. It uses Selenium WebDriver to log in, navigate the dashboard, and populate weekly entries from a JSON file.

 Get your prompt here -----> https://shreyas445.github.io/VTU-Internship-diary-Automation/
1. Enter the required details in the above website
2. Generate the prompt and copy it
3. Paste the prompt in any AI websites like ChatGPT, Gemini etc
4. Copy the json code given by the AI and paste it in the `internship_diary_entries.json` file
5. Change `credentials.json` to your actual email and password
6. save and run `python fill_diary.py` in your terminal

## 🚀 Features

*   **Automated Login**: Securely logs in using credentials stored in a local JSON file.
*   **Batch Processing**: Automatically fills entries for all day in one go.
*   **Smart Selection**: Handles dropdowns for Project, Year, and Month, and dynamically picks the correct Day from the calendar.
*   **Robust Form Filling**: Populates "Work Summaries", "Hours Worked", "Learnings/Outcomes", and handles multi-select "Skills Used".
*   **Error Handling**: Includes retry logic and fallback mechanisms for tricky web elements.

## 📋 Prerequisites

*   [Python 3.x](https://www.python.org/downloads/) installed on your system.
*   Google Chrome browser installed.
*   An active account on the [VTU Internyet Portal](https://vtu.internyet.in/).

## 🛠️ Installation

1.  **Clone this repository** (or download the files):
    ```bash
    git clone https://github.com/Shreyas445/VTU-Internship-diary-Automation
    ```

2.  **Install Dependencies**:
    Run the following command to install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

### 1. Credentials
Create a file named `credentials.json` in the same directory as the script. **Do not commit this file to GitHub.**

**`credentials.json`**:
```json
{
    "email": "YOUR_EMAIL",
    "password": "YOUR_PASSWORD"
}
```

### 2. Diary Entries
Edit the `internship_diary_entries.json` file to include your specific weekly updates. Ensure the date format is `DD-MM-YYYY`.

**`internship_diary_entries.json`** (Example):
```json
[
  {
    "day": 1,
    "date": "11-02-2025",
    "work_summary": "Literature survey and problem definition...",
    "hours_worked": 6.0,
    "learnings_outcomes": "Understood the core requirements...",
    "skills_used": ["Python", "Research"]
  },
  ...
]
```

## 📝 Generating Entries with AI

Don't want to type your entries manually? We've created a custom web tool to easily generate the perfect prompt for AI chatbots (like ChatGPT, Gemini, or Claude).

1. **Open `index.html`** in your web browser.
2. Fill in your Company Name, Domain, Internship Dates, and a brief explanation of your work.
3. Select your preferred input method (Day by Day, Week by Week, or Month by Month).
4. Add your logs (leave blanks if unsure; the AI will intelligently infer realistic tasks to fill the gaps).
5. Click **Generate AI Prompt** and copy the resulting text.
6. **Paste the prompt** into your favorite AI chatbot.
7. **Copy the JSON output** from the AI and save it exactly as `internship_diary_entries.json` in the project folder.

## ▶️ Usage

1.  Make sure you have your `credentials.json` and `internship_diary_entries.json` ready.
2.  Run the script:
    ```bash
    python fill_diary.py
    ```
3.  The browser will open and perform the following actions:
    *   Log in to the portal.
    *   Navigate to the Internship Diary section.
    *   Loop through each week in your JSON file, filling out the details and saving the entry.
4.  Once finished, the terminal will prompt you to press **Enter** to close the browser.

## ⚠️ Important Notes

*   **XPaths**: This script uses specific XPaths for the VTU portal elements. If the portal's design changes, these XPaths in `fill_diary.py` might need updating.
*   **Execution Speed**: `time.sleep()` delays are added to ensure the website processes clicks and animations. Do not remove them, or the script might fail.
*   **Browser Window**: Do not minimize the browser window while the script is running, as some elements require focus to be interacted with.

## 👨‍💻 Developer

Developed by **Shreyas**
- **GitHub**: [https://github.com/Shreyas445](https://github.com/Shreyas445)
- **Repo**: [https://github.com/Shreyas445/VTU-Internship-diary-Automation](https://github.com/Shreyas445/VTU-Internship-diary-Automation)

## 🤝 Contributing

Feel free to fork this project and submit pull requests if you find better ways to handle valid element selection or optimize the flow!

## 📜 Disclaimer & Terms of Use

**Please read this section carefully before using the software.**

### 1. No Responsibility
This software is provided "as is" without any guarantees or warranty. In association with the product, the developer (**Shreyas445**) makes no warranties of any kind, either express or implied, including but not limited to warranties of merchantability, fitness for a particular purpose, of title, or of non-infringement of third-party rights. Use of the software by a user is at the user’s risk.

**The developer is NOT responsible for:**
*   Any academic penalties, rejections, or disciplinary actions faced by the user.
*   Data loss, account bans, or technical issues on the VTU portal.
*   Misuse of this tool for spamming or malicious activities.
*   Any "bad things" that happen as a result of using this automation script.

### 2. Educational Purpose Only
This tool is intended solely for **educational purposes** to demonstrate Python Selenium automation capabilities. It is not intended to bypass any security measures or violate the terms of service of the VTU Internship Portal. Users are responsible for ensuring their use of this tool complies with all relevant university regulations and laws.

### 3. Privacy Policy
*   **Local Execution**: This script runs entirely on your local machine.
*   **No Data Collection**: The developer does **not** collect, store, or transmit any of your personal data, login credentials (`credentials.json`), or diary entries.
*   **Credentials Security**: Your `credentials.json` file remains on your computer. You are responsible for keeping this file secure and not sharing it publicly (e.g., do not commit it to GitHub).

## 🐌 if your looking for project diary automation
click here ----> https://github.com/Shreyas445/VTU-Project-Diary-Automation


## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
