from app.llm import EmbedCluster
from app.scraping import ReviewScraper
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

class ReviewAnalysisPipeline():
   def __init__(self):
      self.embed_cluster = EmbedCluster()
      self.review_scraper = ReviewScraper()
      self.sentiment_analyzer = SentimentIntensityAnalyzer()
      
   def get_saved_reviews(self, filename):
      try:
         with open(filename, 'r') as f:
            data = json.load(f)
         return data
      except FileNotFoundError:
         print("Error: data.json not found.")
      except json.JSONDecodeError:
         print("Error: Invalid JSON format in data.json.")
   
   def get_sentiment_by_rating(self, star_rating: float):
      """Classifies sentiment based on a product's star rating."""
        
      # Ensure star_rating is a number
      if not isinstance(star_rating, (int, float)):
          return "Neutral" # Default for missing ratings
      if star_rating <= 3.0:
          return "Negative"
      elif star_rating >= 4.0:
          return "Positive"
      else: # This handles 3-star reviews
          return "Neutral"
      
   def run_pipeline(self, url):
      reviews = self.review_scraper.get_reviews(url)["reviews"]
      with open("keyboard_reviews.json", "w") as f:
         json.dump(reviews, f, indent=4)
      positive_reviews = []
      negative_reviews = []

      for review in reviews:
         review_text = review["text"]
         star_rating = review["rating"]
         if not review_text or star_rating is None:
               continue

         sentiment = self.get_sentiment_by_rating(star_rating)
         
         if sentiment == "Positive":
               positive_reviews.append(review_text)
         elif sentiment == "Negative":
               negative_reviews.append(review_text)
      
      print(f"Found {len(positive_reviews)} positive reviews and {len(negative_reviews)} negative reviews.")
      print(negative_reviews)

      if positive_reviews:
         print("\n--- Clustering Positive Reviews ---")
         positive_clusters, positive_cluster_num = self.embed_cluster.cluster_reviews(positive_reviews, min(len(positive_reviews), 10))
         positive_clusters = positive_clusters.tolist()
      if negative_reviews:
         print("\n--- Clustering Negative Reviews ---")
         negative_clusters, negative_cluster_num = self.embed_cluster.cluster_reviews(negative_reviews, min(len(negative_reviews), 10))
         negative_clusters = negative_clusters.tolist()
      
      self.save_reviews_clusters(positive_reviews, positive_clusters, "postive_pairings.json")
      self.save_reviews_clusters(negative_reviews, negative_clusters, "negative_pairings.json")
      
      positive_map = [[] for _ in positive_cluster_num]
      for i in range(len(positive_reviews)):
         cluster_number = positive_clusters[i]
         positive_map[cluster_number].append(positive_reviews[i])
      negative_map = [[] for _ in negative_cluster_num]
      for i in range(len(negative_reviews)):
         cluster_number = negative_clusters[i]
         negative_map[cluster_number].append(negative_reviews[i])
         
      
   def save_reviews_clusters(self, reviews, clusters, filename):
      pairings = []
      for i in range(len(reviews)):
         pairings.append({
               "review": reviews[i],
               "cluster": clusters[i]
         })
         
      with open(filename, "w") as f:
         json.dump(pairings, f, indent=4)
         
def main():
   url = "https://www.amazon.com/Wireless-Keyboard-SQMD-Typewriter-Windows/dp/B0DNYK8M7B/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.ORTWL3d7znfuiIiBr8bDzc-CfnkGUE3fSDTF96Mimxra9cVw3lAuWUSBLMJnZmyJSPScvhiPUgH8ay8gYKXV5KQs-D0QgfcXzZ-ydzxqKBf0_TBTq91kEJiP4jBVVLQHtRQaBAVJN_WOTyrszOA-xUYrvqWPBoAR9Gmib8qyZlu3nqNAdBoHYrJLQ46fWhj5LfZqItfTx9LQov7nGyKvIxNpThEXSDUgsyhBd9iPV8ooncjFzJK0DfOYDS0xGaocGIAXQIu0uDtyhzUpQ7sihVIgvS5YgW4vMhhK7-4Vul0.LJSBKrAhRVG-8BJwhGgrAbt1Cg-imxHpm5Oe_GB6K4U&dib_tag=se&hvadid=693645020395&hvdev=c&hvexpln=67&hvlocphy=9004345&hvnetw=g&hvocijid=8191500413380644699--&hvqmt=e&hvrand=8191500413380644699&hvtargid=kwd-299418638870&hydadcr=8474_13653494&keywords=amazon%2Bkeyboard&mcid=b80ee91c22f5326291c51a3b7cb5f4f7&qid=1753048908&s=mobile-apps&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
   pipeline_class = ReviewAnalysisPipeline()
   pipeline_class.run_pipeline(url)
   
if __name__ == "__main__":
   main()