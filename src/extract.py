import pandas as pd

def get_info():
    data_annotated = pd.read_csv("./data/extracted.csv")
    links = pd.read_csv("./data/final_1000.csv")

    merged = data_annotated.merge(links[["URL"]], on="URL", how="inner")

    df = merged[["Title", "Description", "URL"]].rename(
        columns={"Title": "title", "Description": "description", "URL": "url"}
    )

    df.to_csv("./data/word_cloud.csv", index=False)

get_info()