import csv
import glob
import os

input_dir = "./csv"
output_path = "./data/extracted.csv"

def process_line(line: str):
    line = line.rstrip("\n")
    if not line.strip():
        return None

    # find the YouTube URL inside the line
    # url_start = line.find("https://www.youtube.com/")
    url_start = line.find("https://reddit.com")
    if url_start == -1:
        # if you also have youtu.be links, handle them too:
        url_start = line.find("https://youtu.be/")
        if url_start == -1:
            return None

    left = line[:url_start]          # title, video_id, channel, published
    right = line[url_start:]         # URL, description, numeric fields

    # left side: title can have commas, but the last 3 columns are
    # video_id, channel, published_at
    left_parts = left.split(",")
    if len(left_parts) < 4:
        return None

    title = ",".join(left_parts[:-3]).strip()
    # we do not actually need video_id/channel/published here
    # video_id = left_parts[-3]
    # channel = left_parts[-2]
    # published = left_parts[-1]

    # right side: first comma separates URL from the rest
    try:
        url, rest = right.split(",", 1)
    except ValueError:
        return None
    url = url.strip().strip('"')

    # rest = description + 4 numeric columns
    # split from the right to peel off the 4 numeric fields
    parts_from_right = rest.rsplit(",", 4)
    if len(parts_from_right) < 5:
        # no numeric fields, treat everything as description
        description = rest.strip().strip('"')
    else:
        description = parts_from_right[0].strip().strip('"')

    if not url:
        return None

    return title, url, description

csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

with open(output_path, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["Title", "URL", "Description"])

    for path in csv_files:
        with open(path, encoding="utf-8") as f_in:
            first = True
            for raw_line in f_in:
                # skip header line
                if first and "Title" in raw_line and "Video ID" in raw_line:
                    first = False
                    continue
                first = False

                result = process_line(raw_line)
                if result is None:
                    continue
                title, url, description = result
                writer.writerow([title, url, description])