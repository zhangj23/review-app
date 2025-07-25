from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

class EmbedCluster():
   def __init__(self):
      self.model = SentenceTransformer('all-MiniLM-L6-v2')
      
   def cluster_reviews(self, reviews):
      embeddings = self.model.encode(reviews)
      num_clusters = 10
      kmeans = KMeans(n_clusters=num_clusters)
      kmeans.fit(embeddings)
      
      cluster_assignments = kmeans.labels_
      
      return cluster_assignments