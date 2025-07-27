from selenium import webdriver
import os

# --- Setup the Chrome Options ---
options = webdriver.ChromeOptions()

# Your Chrome version

# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "chrome_profile")

# Use a dedicated, non-conflicting profile for scraping
options.add_argument(f'--user-data-dir={profile_path}')
options.add_argument(f'--profile-directory=ScrapingProfile') # Changed from "Default"

# --- Launch the browser ---
print("Initializing Selenium driver...")
driver = webdriver.Chrome(options=options)
print("Driver initialized successfully.")

print("Attempting to navigate to Amazon...")
driver.get("https://www.amazon.com/ap/signin")
print("Navigation command sent. Check the browser window.")

# The script will pause here until you press Enter in the terminal
input("Browser is open. Press Enter in this terminal to close it...") 

print("Script finished.")
driver.quit()