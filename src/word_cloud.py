import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import re
from collections import Counter

def generate_wordcloud(df, text_columns=["Title"], min_freq=5):
    """
    Generate and display a word cloud from specified text columns in a DataFrame.
    No stemming. Words appear exactly as written (after cleaning).
    """

    stopwords = set(STOPWORDS)

    # Combine all selected columns into one text blob
    combined_text = ""
    for col in text_columns:
        if col in df.columns:
            combined_text += " ".join(df[col].dropna().astype(str)) + " "

    # Lowercase and basic cleaning
    combined_text = combined_text.lower()
    combined_text = re.sub(r'\d+', '', combined_text)          # remove numbers
    combined_text = re.sub(r'[^\w\s]', '', combined_text)      # remove punctuation

    # Tokenize
    words = combined_text.split()

    # Remove stopwords, keep normal words
    cleaned_words = [word for word in words if word not in stopwords]

    # Count frequency
    word_counts = Counter(cleaned_words)

    # Filter by frequency
    filtered_counts = {w: c for w, c in word_counts.items() if c >= min_freq}

    # Build word cloud
    wc = WordCloud(width=800, height=400, background_color="white")
    wc.generate_from_frequencies(filtered_counts)

    # Plot and save
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Word Cloud of Reddit Video Descriptions", fontsize=18)
    plt.savefig("reddit_wordcloud.png")
    print("Saved word cloud as reddit_wordcloud.png")

# Run
df = pd.read_csv("./data/Reddit_Final.csv")
generate_wordcloud(df)