import pandas as pd
import matplotlib.pyplot as plt
import re

from collections import Counter
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS

def generate_wordcloud(df, text_columns, min_freq=5):
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
    plt.title("Word Cloud of TikTok Video Descriptions", fontsize=18)
    plt.savefig("tiktok_wordcloud.png")
    print("Saved word cloud as tiktok_wordcloud.png")

# Run, make sure to put all csv's in /data and this will generate
folder_path = Path('./data').glob('*')

# Make columns of main df the same as the first csv so we can match
cols = pd.read_csv("./data/tiktok_AlkalineDiet_20250215.csv", nrows=0).columns
main_df = pd.DataFrame(columns=cols)

for csv in folder_path:
    old_df = pd.read_csv(csv)

    # Append all rows from other CSV's into the main df excluding the header column labels (set above)
    main_df = pd.concat([main_df, old_df.iloc[1:]], ignore_index=True)

# If the header columns are for some reason different from what you sent me then change the column it 
# Makes the wordcloud from
generate_wordcloud(main_df, text_columns=["Description"])
