from app.llm import EmbedCluster
from app.scraping import ReviewScraper

class ReviewAnalysisPipeline():
   def __init__(self):
      self.embed_cluster = EmbedCluster()
      self.review_scraper = ReviewScraper()
   def run_pipeline(self, url):
      reviews = self.review_scraper.get_reviews(url)
      print(reviews)
      clusters = self.embed_cluster.cluster_reviews(reviews["reviews"])
      print(clusters)
      
def main():
   url = "https://www.amazon.com/Wireless-Keyboard-SQMD-Typewriter-Windows/dp/B0DNYK8M7B/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.ORTWL3d7znfuiIiBr8bDzc-CfnkGUE3fSDTF96Mimxra9cVw3lAuWUSBLMJnZmyJSPScvhiPUgH8ay8gYKXV5KQs-D0QgfcXzZ-ydzxqKBf0_TBTq91kEJiP4jBVVLQHtRQaBAVJN_WOTyrszOA-xUYrvqWPBoAR9Gmib8qyZlu3nqNAdBoHYrJLQ46fWhj5LfZqItfTx9LQov7nGyKvIxNpThEXSDUgsyhBd9iPV8ooncjFzJK0DfOYDS0xGaocGIAXQIu0uDtyhzUpQ7sihVIgvS5YgW4vMhhK7-4Vul0.LJSBKrAhRVG-8BJwhGgrAbt1Cg-imxHpm5Oe_GB6K4U&dib_tag=se&hvadid=693645020395&hvdev=c&hvexpln=67&hvlocphy=9004345&hvnetw=g&hvocijid=8191500413380644699--&hvqmt=e&hvrand=8191500413380644699&hvtargid=kwd-299418638870&hydadcr=8474_13653494&keywords=amazon%2Bkeyboard&mcid=b80ee91c22f5326291c51a3b7cb5f4f7&qid=1753048908&s=mobile-apps&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
   pipeline_class = ReviewAnalysisPipeline()
   pipeline_class.run_pipeline(url)
   
if __name__ == "__main__":
   main()