from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver  as uc
import time
import os

class ReviewScraper():
    def __init__(self):
        options = uc.ChromeOptions()
        # Get the absolute path to the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(script_dir, "chrome_profile")

        # Use a dedicated, non-conflicting profile for scraping
        options.add_argument(f'--user-data-dir={profile_path}') 
        options.add_argument(r'--profile-directory=ScrapingProfile')
        self.driver = webdriver.Chrome(options=options)
    def get_reviews(self, url: str):
        reviews = []
        self.driver.get(url)
        # self.pass_captcha()
        time.sleep(5)
        
        self._get_page_reviews(reviews)
        product = self.driver.find_element(By.ID, "productTitle").text
        self.driver.find_element(By.CSS_SELECTOR, "a[data-hook='see-all-reviews-link-foot']").click()
        
        time.sleep(2)
        next_button = self.driver.find_element(By.CLASS_NAME, "a-last")
        while next_button:
            self._get_page_reviews(reviews)
            next_button.click()
            time.sleep(2)
            next_button = self.driver.find_element(By.CLASS_NAME, "a-last")
            if 'a-disabled' in next_button.get_attribute('class').split():
                self._get_page_reviews(reviews)
                break
        time.sleep(2)
        for review in reviews:
            print(review)
        self.driver.quit()
        
        return {
            "reviews": reviews,
            "product": product
        }
        
    def pass_captcha(self):
        time.sleep(0.1)
        self.driver.find_element(By.CLASS_NAME, "a-button-text").click()
    def _get_page_reviews(self, reviews):
        elements = self.driver.find_elements(By.CLASS_NAME, "review-text-content")
        for element in elements:
            reviews.append(element.text)
        
def main():
    url = "https://www.amazon.com/Wireless-Keyboard-SQMD-Typewriter-Windows/dp/B0DNYK8M7B/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.ORTWL3d7znfuiIiBr8bDzc-CfnkGUE3fSDTF96Mimxra9cVw3lAuWUSBLMJnZmyJSPScvhiPUgH8ay8gYKXV5KQs-D0QgfcXzZ-ydzxqKBf0_TBTq91kEJiP4jBVVLQHtRQaBAVJN_WOTyrszOA-xUYrvqWPBoAR9Gmib8qyZlu3nqNAdBoHYrJLQ46fWhj5LfZqItfTx9LQov7nGyKvIxNpThEXSDUgsyhBd9iPV8ooncjFzJK0DfOYDS0xGaocGIAXQIu0uDtyhzUpQ7sihVIgvS5YgW4vMhhK7-4Vul0.LJSBKrAhRVG-8BJwhGgrAbt1Cg-imxHpm5Oe_GB6K4U&dib_tag=se&hvadid=693645020395&hvdev=c&hvexpln=67&hvlocphy=9004345&hvnetw=g&hvocijid=8191500413380644699--&hvqmt=e&hvrand=8191500413380644699&hvtargid=kwd-299418638870&hydadcr=8474_13653494&keywords=amazon%2Bkeyboard&mcid=b80ee91c22f5326291c51a3b7cb5f4f7&qid=1753048908&s=mobile-apps&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
    scraper = ReviewScraper()
    scraper.get_reviews(url)
    
    
if __name__ == "__main__":
    main()