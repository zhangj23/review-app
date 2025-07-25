from sentence_transformers import SentenceTransformer

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your list of reviews
reviews = ["The battery life is amazing!", "The screen is too dim.", "Lasts all day on a single charge."]

# Generate embeddings
embeddings = model.encode(reviews)