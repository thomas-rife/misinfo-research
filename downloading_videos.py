import pandas as pd
import subprocess
import os

def get_unique_videos(df):
    videos = []
    counter = 1

    for _, row in df.iterrows():
        url = row["URL"] if "URL" in df.columns else row["url"]

        if pd.notna(url):
            videos.append((counter, url))
            counter += 1

    return videos

def download_videos(videos, folder):
    os.makedirs(folder, exist_ok=True)
    archive_path = os.path.join(folder, "downloaded.txt")
    print(f"Downloading {len(videos)} videos to folder: {folder}")

    for video_num, url in videos:
        print(f"Downloading: {url} (File ID: {video_num})")

        output_template = os.path.join(folder, f"Reddit_{video_num}.%(ext)s")

        result = subprocess.run([
            "yt-dlp",
            "-o", output_template,
            "--merge-output-format", "mp4",
            "--download-archive", archive_path,
            "--sleep-requests", "1",
            "--sleep-interval", "5",
            "--max-sleep-interval", "15",
            url
        ])

        # If yt-dlp failed, print the failing URL
        if result.returncode != 0:
            print(f"FAILED TO DOWNLOAD: {url}")

reddit_df = pd.read_csv("reddit.csv", encoding="latin1")
reddit_links = get_unique_videos(reddit_df)
print("Unique URLs:", reddit_df['URL'].nunique())

dupes = reddit_df['URL'].value_counts()

download_videos(reddit_links, "reddit_videos")
