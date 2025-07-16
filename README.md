# Selenium Teams Scraper

This Python script uses Selenium to automate interactions with Microsoft Teams. It can be configured to either launch a new Chrome instance or connect to an existing one, allowing for easier debugging and interaction with an already logged-in session.

The script waits for a user to press the `ENTER` key before it proceeds to scrape chat content, giving you full control over the timing. It securely manages your credentials using a `.env` file and uses `undetected-chromedriver` to appear more like a regular user, reducing the chances of being blocked.

-----

## ✨ Features

  * **Secure Credential Management**: Loads email and password from a `.env` file instead of hardcoding them in the script.
  * **Two Launch Modes**:
    1.  **New Browser**: Launches a new, clean instance of Chrome for the automation.
    2.  **Connect to Existing Browser**: Attaches to an already running Chrome instance (requires launching Chrome with a remote debugging port).
  * **Manual Trigger**: Waits for the user to press the `ENTER` key before initiating the scraping logic, giving you time to navigate to the correct chat or channel.
  * **Stealth Operations**: Uses `undetected-chromedriver` to avoid bot detection.
  * **Robust Automation**: Employs explicit waits to handle page load times gracefully, preventing common script failures.
  * **Organized Output**: Saves the scraped chat content to a timestamped text file (e.g., `teams_chat_2025-07-16_15-30-05.txt`).

-----

## 📋 Prerequisites

  * Python 3.8+
  * Google Chrome browser installed.

-----

## ⚙️ Setup and Configuration

Follow these steps to set up the project environment and configure your credentials.

**1. Clone the Repository**
Clone this repository to your local machine:

```bash
git clone https://github.com/QuiteUncertain/selenium_teams.git
cd selenium_teams
```

**2. Create a Virtual Environment (Recommended)**
It's highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Create the Configuration File**
Create a file named `.env` in the root of the project directory. This file will store your Microsoft Teams credentials securely.

Your `.env` file should look like this:

```
# .env file
TEAMS_EMAIL="your-email@example.com"
TEAMS_PASSWORD="your_password_here"
```

**Important**: The included `.gitignore` file is configured to ignore the `.env` file, so your credentials will not be accidentally committed to version control.

-----

## ▶️ Usage

You can run the script in two primary modes.

### Mode 1: Launch a New Browser Instance (Default)

This mode will open a fresh Chrome window and attempt to log in using the credentials from your `.env` file.

To run in this mode, simply execute the script:

```bash
python selenium_teams.py
```

### Mode 2: Connect to an Existing Chrome Session

This mode is useful for development or if you are already logged into Teams. It allows the script to take control of a Chrome tab you already have open, bypassing the login process.

**Step 1: Launch Chrome with Remote Debugging**
You must first close all running instances of Google Chrome. Then, launch it from your terminal with a special flag.

  * **On Windows (using Command Prompt):**

    ```cmd
    "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
    ```

  * **On macOS (using Terminal):**

    ```bash
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
    ```

  * **On Linux (using Terminal):**

    ```bash
    google-chrome --remote-debugging-port=9222
    ```

After running this command, open Teams in your browser and navigate to the desired page.

**Step 2: Run the Python Script with the `--connect` Flag**
Open a new terminal, navigate to the project directory, and run the script with the `--connect` flag:

```bash
python selenium_teams.py --connect
```

### The Scraping Process

1.  After the script launches (in either mode), it will print:
    `✅ Browser is ready. Navigate to the desired chat and press ENTER to start scraping...`
2.  At this point, manually navigate within the Teams web interface to the chat you want to scrape.
3.  Once ready, press the `ENTER` key in the terminal where the script is running.
4.  The script will then scrape the visible chat content and save it to a timestamped `.txt` file in the project directory.

-----

## ⚠️ Disclaimer

This script is for educational purposes only. Be aware of the terms of service for Microsoft Teams. Automating user accounts can be against the terms of service and may lead to account restrictions. Use this script responsibly and at your own risk.
