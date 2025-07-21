import undetected_chromedriver as uc
import time

# --- Setup the Chrome Options ---
options = uc.ChromeOptions()

# Set the path to your user profile. This will create the folder if it doesn't exist.
options.add_argument(r'--user-data-dir=C:\Users\Justin\OneDrive\Documents\GitHub\review-app\scraping\chrome_profile') 

# Provide a profile name
options.add_argument(r'--profile-directory=Default')

# --- Launch the browser with the options ---
driver = uc.Chrome(options=options)

print("Opening Amazon... If you are not logged in, please log in manually in the browser window.")
driver.get("https://www.amazon.com/errors/login") # A page to check your login status

# Keep the browser open for a bit so you can see the result or log in
time.sleep(300) 

print("Script finished. Your session is now saved in the 'chrome_profile' folder.")
driver.quit()