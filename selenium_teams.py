# selenium_teams.py

import os
import argparse
import time
from datetime import datetime

import keyboard
import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- Configuration ---
# Load credentials and settings from the .env file
load_dotenv()
TEAMS_EMAIL = os.getenv("TEAMS_EMAIL")
TEAMS_PASSWORD = os.getenv("TEAMS_PASSWORD")
TEAMS_URL = "https://teams.microsoft.com"

# Using more stable 'data-tid' attributes for selectors where possible
LOCATORS = {
    "email_field": (By.ID, "i0116"),
    "next_button": (By.ID, "idSIButton9"),
    "password_field": (By.ID, "i0118"),
    "no_button": (By.ID, "idBtn_Back"),
    "chat_pane": (By.ID, "chat-pane-list"),
    "chat_messages_container": (By.CSS_SELECTOR, "div[data-tid='message-pane-list-content']"),
    "message_group": (By.CSS_SELECTOR, "div[data-tid^='message-']"),
    "message_author": (By.CSS_SELECTOR, "div[data-tid='message-author']"),
    "message_timestamp": (By.CSS_SELECTOR, "span.timestamp"),
    "message_body": (By.CSS_SELECTOR, "div.message-body-content"),
}


def get_webdriver(connect_to_existing: bool) -> uc.Chrome:
    """Initializes and returns a Selenium WebDriver instance."""
    options = uc.ChromeOptions()

    if connect_to_existing:
        print("▶️ Attempting to connect to existing Chrome instance on port 9222...")
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    else:
        print("🚀 Launching a new Chrome instance...")

    try:
        driver = uc.Chrome(options=options, version_main=108)
        driver.implicitly_wait(5) # Set a base implicit wait
    except Exception as e:
        print(f"❌ Error initializing WebDriver: {e}")
        print("Ensure Chrome is running with '--remote-debugging-port=9222' if using --connect.")
        return None
        
    return driver


def login(driver: uc.Chrome):
    """Handles the login process for Microsoft Teams."""
    try:
        print("🔐 Starting login process...")
        wait = WebDriverWait(driver, 20)

        # Enter email
        email_field = wait.until(EC.visibility_of_element_located(LOCATORS["email_field"]))
        email_field.send_keys(TEAMS_EMAIL)
        driver.find_element(*LOCATORS["next_button"]).click()
        print("    -> Email submitted.")

        # Enter password
        password_field = wait.until(EC.visibility_of_element_located(LOCATORS["password_field"]))
        password_field.send_keys(TEAMS_PASSWORD)
        driver.find_element(*LOCATORS["next_button"]).click()
        print("    -> Password submitted.")
        
        # Handle "Stay signed in?" prompt
        no_button = wait.until(EC.visibility_of_element_located(LOCATORS["no_button"]))
        no_button.click()
        print("    -> Handled 'Stay signed in?' prompt.")
        
        # Wait for the main chat interface to load
        wait.until(EC.visibility_of_element_located(LOCATORS["chat_pane"]))
        print("✅ Login successful!")

    except Exception as e:
        print(f"❌ Login failed. The page structure may have changed. Error: {e}")


def scrape_current_chat(driver: uc.Chrome):
    """Scrapes all messages from the currently open chat pane."""
    print("\n scraping chat content...")
    wait = WebDriverWait(driver, 10)
    
    try:
        # Wait for the message container to be present
        message_container = wait.until(EC.presence_of_element_located(LOCATORS["chat_messages_container"]))
        
        # Find all message groups within the container
        message_groups = message_container.find_elements(*LOCATORS["message_group"])
        
        if not message_groups:
            print("No messages found in the current chat.")
            return

        # Prepare filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"teams_chat_{timestamp}.txt"
        
        scraped_count = 0
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Scraped from: {driver.title}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 40 + "\n\n")

            for group in message_groups:
                try:
                    # Extract author, timestamp, and message body from each message
                    author = group.find_element(*LOCATORS["message_author"]).text
                    timestamp = group.find_element(*LOCATORS["message_timestamp"]).get_attribute('title')
                    body = group.find_element(*LOCATORS["message_body"]).text
                    
                    f.write(f"[{timestamp}] {author}:\n")
                    f.write(f"{body}\n")
                    f.write("-" * 20 + "\n")
                    scraped_count += 1
                except Exception:
                    # Skip elements that aren't full messages (e.g., "You joined the chat")
                    continue
        
        print(f"✅ Success! Scraped {scraped_count} messages to '{filename}'")

    except Exception as e:
        print(f"❌ Failed to scrape chat. Could not find message elements. Error: {e}")


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Scrape Microsoft Teams chat content.")
    parser.add_argument(
        "--connect",
        action="store_true",
        help="Connect to an existing Chrome session instead of launching a new one."
    )
    args = parser.parse_args()

    driver = get_webdriver(connect_to_existing=args.connect)
    if not driver:
        return
        
    if not args.connect:
        driver.get(TEAMS_URL)
        login(driver)
    
    print("\n" + "="*50)
    print("✅ Browser is ready. Navigate to the desired chat.")
    print("   Press the ENTER key in this terminal to start scraping.")
    print("="*50)

    # Wait for the user to press Enter before proceeding
    keyboard.wait("enter")
    
    scrape_current_chat(driver)
    
    # Keep the browser open for inspection after script finishes
    print("\nScript finished. Browser will remain open. Close it manually.")
    # uncomment the line below to automatically close the browser
    # driver.quit()


if __name__ == "__main__":
    main()
