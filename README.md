# AI-Powered Product Review Analyzer

This project is an end-to-end data science pipeline that automatically scrapes, analyzes, and summarizes hundreds of product reviews from e-commerce sites. It uses unsupervised machine learning to discover key topics and leverages a Large Language Model (LLM) to generate a concise, actionable report of top pros and cons.

## The Problem

Online shoppers face a significant challenge: information overload. A popular product can have thousands of reviews, making it impossible to manually read through them all. Furthermore, many reviews are uninformative, and it's difficult to distinguish recurring, legitimate issues from isolated, outlier complaints. This project was built to solve that problem by providing a data-driven summary at a glance.

## Tech Stack

| Category          | Technologies                                                           |
| :---------------- | :--------------------------------------------------------------------- |
| Data Science & AI | Python, Pandas, Scikit-learn, Sentence-Transformers, Google Gemini API |
| Web Scraping      | Selenium, Undetected Chromedriver                                      |
| Core Libraries    | NumPy, Dotenv                                                          |

## The Data Science Pipeline

This project implements a multi-stage pipeline to transform raw, unstructured review text into a structured, insightful report.

### 1. Data Acquisition (Web Scraping)

- A robust web scraper built with Selenium and Undetected Chromedriver navigates dynamic e-commerce product pages.

- It handles pagination to collect hundreds of reviews and their corresponding star ratings, bypassing common anti-bot measures.

- A persistent browser profile is used to manage login sessions, ensuring access to complete review data.

### 2. Sentiment Classification (Rules-Based)

- To avoid the high cost and potential ambiguity of using an LLM for simple sentiment analysis, I implemented a highly efficient, rules-based approach.

- The customer's star rating is used as the "ground truth" for sentiment. Reviews with 4-5 stars are classified as "Positive," and reviews with 1-3 stars are classified as "Negative." This method proved more reliable than lexicon-based tools like VADER, which struggled with nuanced reviews containing mixed sentiment (e.g., "The color is great, but it broke in a week.").

### 3. Unsupervised Topic Modeling (Embeddings & Clustering)

- To discover the hidden themes within the reviews, I employed unsupervised machine learning.

- Embeddings: Each review is converted into a 384-dimension numerical vector using the all-MiniLM-L6-v2 model from the Sentence-Transformers library. These vectors represent the semantic meaning of the text, placing reviews with similar topics close together in a high-dimensional space.

- Clustering: The K-Means algorithm from Scikit-learn is then used to group these vectors into distinct clusters. Each cluster represents a specific pro or con (e.g., "battery life," "screen quality").

### 4. Dynamic Cluster Optimization (Silhouette Score)

- To avoid hardcoding the number of topics, I implemented a data-driven method to find the optimal number of clusters for any given set of reviews.

- The Silhouette Score is calculated for a range of cluster counts. This score measures how well-defined the clusters are by evaluating how close each point is to its own cluster compared to others. The number of clusters that yields the highest score is then used for the final analysis, ensuring the topics are mathematically significant.

- I also implemented a floor for the cluster count to ensure sufficient granularity in the final topics, preventing overly broad categories.

### 5. Semantic Summarization (LLM)

- With the reviews cleanly grouped by topic, the final step is to generate a human-readable title for each cluster.

- A small, representative sample of reviews from each of the top 5 positive and negative clusters is sent to the Google Gemini API.

- A carefully engineered prompt instructs the LLM to act as a product analyst and return a concise, 2-4 word title for the specific feature being discussed, resulting in a clean list of top pros and cons.

## How to Run This Project

### 1. Clone the repository:

```
git clone https://github.com/zhangj23/review-app.git
cd review-app
```

### 2. Set up the environment:

```
# Create a virtual environment
python -m venv .venv
# Activate it
.venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

### 3. Configure your API Key:

Create a .env file in the root directory.

Add your Google Gemini API key to the file:

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4. Run the pipeline:

Open app/main.py and replace the placeholder URL with the Amazon product URL you want to analyze.

Run the script from the root directory:

```
python -m app.main
```
