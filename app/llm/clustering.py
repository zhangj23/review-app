from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class EmbedCluster():
   def __init__(self):
      self.model = SentenceTransformer('all-MiniLM-L6-v2')
      
   def _find_optimal_k(self, embeddings, max_k=15):
        """Finds the optimal number of clusters using the silhouette score."""
        silhouette_scores = []
        cluster_range = range(2, max_k)

        for k in cluster_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
            kmeans.fit(embeddings)
            score = silhouette_score(embeddings, kmeans.labels_)
            silhouette_scores.append(score)
        
        if not silhouette_scores:
            return 5 # Return a default value if no scores were calculated

        # Return the k that corresponds to the highest silhouette score
        return cluster_range[silhouette_scores.index(max(silhouette_scores))]
     
   def cluster_reviews(self, reviews):
      num_clusters = self._find_optimal_k(embeddings)
      
      embeddings = self.model.encode(reviews)
      kmeans = KMeans(n_clusters=num_clusters,  random_state=42, n_init='auto')
      kmeans.fit(embeddings)
      
      
      cluster_assignments = kmeans.labels_
      
      return cluster_assignments, embeddings