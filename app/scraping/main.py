from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import os
import time

class ReviewScraper():
    def __init__(self):
        options = uc.ChromeOptions()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(script_dir, "chrome_profile")

        options.add_argument(f'--user-data-dir={profile_path}') 
        options.add_argument(r'--profile-directory=ScrapingProfile')
        
        self.driver = uc.Chrome(options=options)
        
        self.wait = WebDriverWait(self.driver, 10)

    def get_reviews(self, url: str):
        reviews = []
        try:
            self.driver.get(url)
            
            product_title_element = self.wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
            product = product_title_element.text
            print(f"Scraping reviews for: {product}")

            # Wait for the "see all reviews" link and click it
            see_all_reviews_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-hook='see-all-reviews-link-foot']")))
            see_all_reviews_link.click()

            print("Navigating review pages...")
            page_count = 1
            while True:
                try:
                    print(f"Scraping page {page_count}...")
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='review-star-rating']")))
                    time.sleep(0.5)
                    self._get_page_reviews(reviews)
                    
                    next_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last a")))
                    
                    self.driver.execute_script("arguments[0].click();", next_button)
                    
                    page_count += 1

                except TimeoutException:
                    print("Reached the last page of reviews.")
                    break

            print(f"\nScraped a total of {len(reviews)} reviews.")
            print(reviews)
            return {
                "reviews": reviews,
                "product": product
            }

        except (TimeoutException, NoSuchElementException) as e:
            print(f"A required element was not found on the page, aborting. Error: {e}")
            return {"reviews": [], "product": "Unknown"}
        finally:
            self.close()

    def _get_page_reviews(self, reviews_list: list):
        """Helper function to extract all review text and ratings from the current page."""

        # Find the parent review containers first
        review_containers = self.driver.find_elements(By.CSS_SELECTOR, "[data-hook='review']")

        for container in review_containers:
            try:
                review_text_element = container.find_element(By.CSS_SELECTOR, "span[data-hook='review-body'] span")
                review_text = review_text_element.text
                
                rating_element = container.find_element(By.CSS_SELECTOR, "i[data-hook='review-star-rating'] span")
                
                # Use .get_attribute('textContent') to get the hidden text
                rating_text = rating_element.get_attribute('textContent')

                # Parse the string to get just the number
                rating_value = float(rating_text.split(" ")[0])

                # Append the structured data
                if review_text: # Ensure review text is not empty
                    reviews_list.append({
                        "text": review_text,
                        "rating": rating_value
                    })
            except Exception as e:
                # This will skip any review that is missing a rating or text, preventing crashes
                print(f"Skipping a review due to an error: {e}")

    def close(self):
        """Closes the WebDriver session."""
        print("Closing the browser.")
        self.driver.quit()

def main():
    url = "https://www.amazon.com/dp/B0DNYK8M7B/"
    
    scraper = ReviewScraper()
    scraped_data = scraper.get_reviews(url)
    
    if scraped_data and scraped_data["reviews"]:
        print(f"\nFirst review scraped: '{scraped_data['reviews'][0][:100]}...'")

if __name__ == "__main__":
    main()