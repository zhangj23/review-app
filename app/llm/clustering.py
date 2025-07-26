from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

class EmbedCluster():
   def __init__(self):
      self.model = SentenceTransformer('all-MiniLM-L6-v2')
      
   def cluster_reviews(self, reviews, num_clusters):
      embeddings = self.model.encode(reviews)
      kmeans = KMeans(n_clusters=num_clusters)
      kmeans.fit(embeddings)
      
      cluster_assignments = kmeans.labels_
      
      return cluster_assignments, embeddings