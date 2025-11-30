import pandas as pd
import matplotlib.pyplot as plt
import re

from matplotlib.colors import LinearSegmentedColormap
from collections import Counter
from pathlib import Path
from wordcloud import WordCloud, STOPWORDS

def generate_wordcloud(df, text_columns, min_freq=15):
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
    # print(word_counts["health"])
    # print(word_counts["diet"])
    # print(word_counts["video"])

    # Filter by frequency
    # filtered_counts = {w: c for w, c in word_counts.items() if c >= min_freq}

    filtered_counts = {}
    for word, count in word_counts.items():
        # if count >= 30:
        #     filtered_counts[word] = 30
        if count >= min_freq:
            filtered_counts[word] = count
    
    del filtered_counts["fok"], filtered_counts["dont"]

    # for word, count in filtered_counts.items():
    #     if count == 30:
    #         print(word)
    #         print(count)

    colors = [
    "#1d2b64",  # deep navy
    "#2a3a8a",  # dark blue
    "#3b3c99",  # indigo-blue
    "#4a3f8f",  # muted purple
    "#5b3a7a",  # dark violet
    "#6b2f5f",  # plum
    ]

    cmap = LinearSegmentedColormap.from_list("custom_dark", colors)

    # Build word cloud
    wc = WordCloud(width=2400, height=1200, background_color="white", collocations=True, max_font_size=300, min_font_size=50, colormap=cmap)
    wc.generate_from_frequencies(filtered_counts)

    # Plot and save
    plt.figure(figsize=(12, 6), dpi=250)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=1)  # removes padding inside the figure
    # plt.title("Word Cloud of YouTube Video Descriptions", fontsize=18)
    plt.savefig("wordcloud_youtube.png")
    print("Saved word cloud as youtube_PLATFORM.png")

# Run, make sure to put all csv's in /data and this will generate
folder_path = Path('./data').glob('*')

# Make columns of main df the same as the first csv so we can match
# cols = pd.read_csv("./data/tiktok_AlkalineDiet_20250215.csv", nrows=0).columns
# main_df = pd.DataFrame(columns=cols)

# for csv in folder_path:
#     old_df = pd.read_csv(csv)

#     # Append all rows from other CSV's into the main df excluding the header column labels (set above)
#     main_df = pd.concat([main_df, old_df.iloc[1:]], ignore_index=True)

# If the header columns are for some reason different from what you sent me then change the column it 
# Makes the wordcloud from
main_df = pd.read_csv("./yt_data/word_cloud.csv")
generate_wordcloud(main_df, text_columns=["description"])
