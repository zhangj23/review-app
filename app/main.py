import pandas as pd
import numpy as np
import json
from app.llm import EmbedCluster, GeminiHandler
from app.scraping import ReviewScraper

class ReviewAnalysisPipeline():
    def __init__(self):
        self.embed_cluster = EmbedCluster()
        self.review_scraper = ReviewScraper()
        self.gemini_handler = GeminiHandler()
      
    def get_sentiment_by_rating(self, star_rating: float):
        """Classifies sentiment based on a product's star rating."""
        if not isinstance(star_rating, (int, float)):
            return "Neutral"
        if star_rating <= 3.0:
            return "Negative"
        elif star_rating >= 4.0:
            return "Positive"
        else:
            return "Neutral"
          
    def _analyze_sentiment_group(self, reviews_df, sentiment_type):
        """
        Helper function to perform clustering and topic extraction for a given sentiment group.
        """
        if reviews_df.empty:
            return []

        print(f"\n--- Analyzing {sentiment_type.title()} Reviews ---")
        
        # Get reviews and embeddings
        reviews = reviews_df['text'].tolist()
        embeddings = np.array(self.embed_cluster.model.encode(reviews))
        
        # Perform clustering
        kmeans_model, _, _ = self.embed_cluster.cluster_reviews(reviews)
        reviews_df['cluster'] = kmeans_model.labels_

        # Find the top 5 largest clusters
        top_5_clusters = reviews_df['cluster'].value_counts().nlargest(5).index
        
        topics = []
        for cluster_id in top_5_clusters:
            # Find the reviews closest to the centroid for this cluster
            centroid_reviews = self.embed_cluster._find_reviews_closest_to_centroid(
                kmeans_model, embeddings, reviews, cluster_id, n_reviews=3
            )
            # Use the LLM to generate a topic title
            topic = self.gemini_handler._get_cluster_topic(centroid_reviews, sentiment_type)
            topics.append(topic)
            print(f"  Cluster {cluster_id} ({sentiment_type}): {topic}")
            
        return topics

    def run_pipeline(self, url):
        """Run pipeline that gets pros and cons of a product from a link using Pandas."""
        
        # Step 1: Scrape data and load into a master DataFrame
        # scraped_reviews = self.review_scraper.get_reviews(url)["reviews"]
        with open("keyboard_reviews.json", 'r') as f:
             scraped_reviews = json.load(f)
             
        df = pd.DataFrame(scraped_reviews)
        
        # Step 2: Classify sentiment for each review
        df['sentiment'] = df['rating'].apply(self.get_sentiment_by_rating)
        
        # Step 3: Split the DataFrame into positive and negative groups
        df_pos = df[df['sentiment'] == 'Positive'].copy()
        df_neg = df[df['sentiment'] == 'Negative'].copy()
        
        print(f"Found {len(df_pos)} positive reviews and {len(df_neg)} negative reviews.")
        
        # Step 4: Run the analysis on each group
        final_pros = self._analyze_sentiment_group(df_pos, "pro")
        final_cons = self._analyze_sentiment_group(df_neg, "con")

        print("\n--- FINAL RESULTS ---")
        print("Pros:", final_pros)
        print("Cons:", final_cons)
        
        print("\n--- FINAL REPORT ---")
        print(self.gemini_handler.generate_final_report(final_pros, final_cons))
        # You can easily save the results to a CSV file
        df.to_csv("analyzed_reviews.csv", index=False)
        print("\nSaved full analysis to analyzed_reviews.csv")

        return {"pros": final_pros, "cons": final_cons}

# The main function remains the same
def main():
    url = "https://www.amazon.com/Wireless-Keyboard-SQMD-Typewriter-Windows/dp/B0DNYK8M7B/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.ORTWL3d7znfuiIiBr8bDzc-CfnkGUE3fSDTF96Mimxra9cVw3lAuWUSBLMJnZmyJSPScvhiPUgH8ay8gYKXV5KQs-D0QgfcXzZ-ydzxqKBf0_TBTq91kEJiP4jBVVLQHtRQaBAVJN_WOTyrszOA-xUYrvqWPBoAR9Gmib8qyZlu3nqNAdBoHYrJLQ46fWhj5LfZqItfTx9LQov7nGyKvIxNpThEXSDUgsyhBd9iPV8ooncjFzJK0DfOYDS0xGaocGIAXQIu0uDtyhzUpQ7sihVIgvS5YgW4vMhhK7-4Vul0.LJSBKrAhRVG-8BJwhGgrAbt1Cg-imxHpm5Oe_GB6K4U&dib_tag=se&hvadid=693645020395&hvdev=c&hvexpln=67&hvlocphy=9004345&hvnetw=g&hvocijid=8191500413380644699--&hvqmt=e&hvrand=8191500413380644699&hvtargid=kwd-299418638870&hydadcr=8474_13653494&keywords=amazon%2Bkeyboard&mcid=b80ee91c22f5326291c51a3b7cb5f4f7&qid=1753048908&s=mobile-apps&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
    pipeline = ReviewAnalysisPipeline()
    pipeline.run_pipeline(url)
    
if __name__ == "__main__":
    main()