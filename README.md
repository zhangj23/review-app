# review-app

LLM processing was expensive, so I was trying to figure out ways to reduce token costs.

First I thought of using the map reduce method. Although this method does help with LLM losing the middle of the query, it does not help but instead hinder the cost of using the LLM.

I then found a method called embedding and clustering, where you first tokenize the sentences then assign a large dimensioned vector to the review to categorize it by numbers (384 dimensions in my case). I then used the scikit learn library for the Kmeans model to classify and group together reviews with similar topics. Imagine a 384 dimensioned graph and the Kmeans algorithm just takes the top 10 closely related points in the graph and assigns them each their own number where each point relates to a review.

When clustering and embedding the reviews, I found that pros and the cons were in the same topic, even though their connotations were completely differing. Using vader's sentinment intensity analyzer, I can see seperate the pros and the cons before clustering them together.

I then realized that vader could not differentiate sentences with "but" in them, if the part before the but was more positive than the part after the but, it will be deemed positive even though a human would consider it more negative. This would require an LLM, which was against the point of doing all this anyways, so I had to find a different method. The method was staring at me the whole time, the ratings that the customer left are the best indicator of the sentiment.
