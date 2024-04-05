import streamlit as st
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Initialize Reddit API
reddit = praw.Reddit(client_id='8QWHora2LrjLtsSVMGXt4g',
                     client_secret='OjbA9HvEsgNeSs8jciHBBKjoo5Foig',
                     user_agent='praw_scraper_1.0')

# Function to perform sentiment analysis using VADER
def analyze_sentiment(comment):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(comment)
    compound_score = score['compound']
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Streamlit app
def main():
    st.title("Reddit Comments Sentiment Analyzer")
    st.write("made by - Harry & Harika")

    # Input field for Reddit post URL
    reddit_post_url = st.text_input("Enter Reddit Post URL:")

    if reddit_post_url:
        try:
            # Get Reddit post and comments
            submission = reddit.submission(url=reddit_post_url)
            submission.comments.replace_more(limit=None)
            all_comments = submission.comments.list()
            
            comments = all_comments[-20:]

            # Perform sentiment analysis and store results
            sentiments = [analyze_sentiment(comment.body) for comment in comments]

            # Generate pie chart
            sentiment_counts = {
                'Positive': sentiments.count('Positive'),
                'Negative': sentiments.count('Negative'),
                'Neutral': sentiments.count('Neutral')
            }

            # Plot pie chart
            labels = sentiment_counts.keys()
            sizes = sentiment_counts.values()
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            # Display sentiment analysis results
            st.subheader("Sentiment Analysis Results:")
            st.write(sentiment_counts)

            # Display last 10 comments
            st.subheader("Last 10 Comments:")
            for i, comment in enumerate(comments[:10]):
                st.write(f"Comment {i+1}: {comment.body}")
                st.write(f"Sentiment: {analyze_sentiment(comment.body)}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
