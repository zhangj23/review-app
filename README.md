# review-app

LLM processing was expensive, so I was trying to figure out ways to reduce token costs.
First I thought of using the map reduce method. Although this method does help with LLM losing the middle of the query, it does not help but instead hinder the cost of using the LLM.
I then found a method called embedding and clustering, where you first tokenize the sentences then assign a large dimensioned vector to the review to categorize it by numbers (384 dimensions in my case). I then used the scikit learn library for the Kmeans model to classify and group together reviews with similar topics. Imagine a 384 dimensioned graph and the Kmeans algorithm just takes the top 10 closely related points in the graph and assigns them each their own number where each point relates to a review.
When clustering and embedding the reviews, I found that pros and the cons were in the same topic, even though their connotations were completely differing. Using vader's sentinment intensity analyzer, I can see seperate the pros and the cons before clustering them together.
