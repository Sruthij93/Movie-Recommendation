# Movie Recommender - Personal Project

This is a personal project I worked on after following a YouTube tutorial. The goal of this project was to create a movie recommender app using machine learning. I used various techniques to vectorize the movie data and apply similarity measures to recommend movies based on user preferences.

## Technologies Used:
- **Machine Learning **: For building the recommendation system. Used scikit-learn.
- **Streamlit**: For creating the web app interface.
- **Render**: For deployment, instead of Heroku as suggested in the YouTube tutorial.

## Techniques Applied:
1. **Text Vectorization using Bag of Words**:
   - In the Bag of Words technique, I combined all the tags associated with a movie into a single large text string. From this large text, I calculated the frequency of all the words.
   - The top 5000 words with the highest frequency were extracted to form a feature set.

2. **Stemming**:
   - I applied stemming to remove different forms of the same word. For example, "action," "actions," and "acting" were all treated as "action."

3. **Frequency Calculation**:
   - After stemming, I checked the frequency of these top 5000 words in each movie's tags.
   - A DataFrame was created where the shape was 5000 x 5000 (movies vs. top words), representing the frequency of the top words in each movie's tag.

4. **Stop Words Removal**:
   - Stop words like "and," "to," "the," "from," etc., were removed, as they don't add significant meaning to the text.

5. **Cosine Distance for Similarity**:
   - Once each movie was represented in vector format, I used **Cosine Distance** to measure the similarity between movies. 
   - Cosine Distance is preferred over Euclidean distance in higher-dimensional spaces, as Euclidean distance is not a reliable measure of similarity in such contexts.

Link to the website: https://movie-recommender-1exi.onrender.com

