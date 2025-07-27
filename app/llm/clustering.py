from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
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
      
      return kmeans, num_clusters, embeddings
   
   def _find_reviews_closest_to_centroid(self, kmeans_model, embeddings, reviews, cluster_id, n_reviews=3):
       """
       Finds the n reviews with embeddings closest to a given cluster's centroid.
       """
       # Get the coordinates of the cluster's center
       centroid = kmeans_model.cluster_centers_[cluster_id]
       # Find the indices of all reviews belonging to this cluster
       indices_in_cluster = np.where(kmeans_model.labels_ == cluster_id)[0]
       
       if len(indices_in_cluster) == 0:
           return []
        
       # Get the embeddings for only the reviews in this cluster
       embeddings_in_cluster = embeddings[indices_in_cluster]
       
       # Calculate the distance from each review embedding to the centroid
       distances = np.linalg.norm(embeddings_in_cluster - centroid, axis=1)
       
       # Get the indices of the n reviews with the smallest distances
       closest_indices_in_cluster = np.argsort(distances)[:n_reviews]
       
       # Get the original indices of these reviews from the full list
       original_indices = indices_in_cluster[closest_indices_in_cluster]
       
       # Return the actual review text for the closest reviews
       return [reviews[i] for i in original_indices]