import json
import os
import base64
import requests
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
import zipfile
import csv

from urllib.parse import urlparse
from io import BytesIO
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    AssetIn,
    asset,
    get_dagster_logger,
)

dir_base = 'data/dags/hackernews'


## Top Stories - Data Collect

@asset(group_name="hackernews")
def topstory_ids() -> None:
    """
    Get IDs list of top stories.

    API Docs: https://github.com/HackerNews/API#new-top-and-best-stories.
    """      
    newstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_new_story_ids = requests.get(newstories_url).json()[:100]

    os.makedirs(dir_base, exist_ok=True)
    with open(f"{dir_base}/topstory_ids.json", "w") as f:
        json.dump(top_new_story_ids, f)


@asset(deps=[topstory_ids],group_name="hackernews")
def topstories(context: AssetExecutionContext) -> None:
    """
    Get items based on top story ids.

    API Docs: https://github.com/HackerNews/API#new-top-and-best-stories.
    """    
    logger = get_dagster_logger()

    with open(f"{dir_base}/topstory_ids.json", "r") as f:
        topstory_ids = json.load(f)

    results = []
    for item_id in topstory_ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
        ).json()
        results.append(item)

        if len(results) % 20 == 0:
            logger.info(f"Got {len(results)} items so far.")

    df = pd.DataFrame(results)
    df.to_csv(f"{dir_base}/topstories.csv")

    context.add_output_metadata(
        metadata={
            "num_records": len(df),  # Metadata can be any key-value pair
            "preview": MetadataValue.md(df.head().to_markdown()),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )

## Stopwords - Zip file

@asset(group_name="hackernews")
def stopwords_zip() -> None:
    """
    Download stopword zip file.

    URL: https://docs.dagster.io/assets/stopwords.zip
    """
    urllib.request.urlretrieve(
        'https://docs.dagster.io/assets/stopwords.zip',
        f'{dir_base}/stopwords.zip',
    )

@asset(non_argument_deps={"stopwords_zip"},group_name="hackernews")
def stopwords_csv() -> None:
    """
    Unzip file 'stopwords.zip'
    """
    with zipfile.ZipFile(f'{dir_base}/stopwords.zip', "r") as zip:
        zip.extract('stopwords.csv',f'{dir_base}')    

## Top Stories - Word Counts

@asset(
        deps=[topstories, stopwords_csv],
        group_name="hackernews"
)
def most_frequent_words(context: AssetExecutionContext) -> pd.DataFrame:
    """
    Incorporates a bar chart of the most frequently used words as metadata.
    """    
    local_stopwords = {"ai", "the", "an", "of", "to", "in", 
                       "for", "and", "with", "on", "is", "yc",
                       "s23", "x", "far", "this", "than"}

    with open(f'{dir_base}/stopwords.csv', 'r') as f:
        stopwords = {row[0] for row in csv.reader(f)}

    num_stopwords = len(stopwords)

    stopwords = stopwords.union(local_stopwords)

    topstories = pd.read_csv(f"{dir_base}/topstories.csv")

    # loop through the titles and count the frequency of each word
    word_counts = {}
    for raw_title in topstories["title"]:
        title = raw_title.lower()
        for word in title.split():
            cleaned_word = word.strip(".,-!?:;()[]'\"–")
            if cleaned_word not in stopwords and len(cleaned_word) > 0:
                word_counts[cleaned_word] = word_counts.get(cleaned_word, 0) + 1

    # Get the top 25 most frequent words
    top_words = {
        pair[0]: pair[1]
        for pair in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:25]
    }

    # Make a bar chart of the top 25 words
    plt.figure(figsize=(10, 6))
    plt.bar(top_words.keys(), top_words.values())
    plt.xticks(rotation=45, ha="right")
    plt.title("Top 25 Words in Hacker News Titles")
    plt.tight_layout()

    # Convert the image to a saveable format
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())

    # Convert the image to Markdown to preview it within Dagster
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    with open(f"{dir_base}/most_frequent_words.json", "w") as f:
        json.dump(top_words, f)

    # Attach the Markdown content as metadata to the asset
    context.add_output_metadata(
        metadata={
            "dload_stopwords": num_stopwords,
            "local_stopwords": len(local_stopwords),
            "total_stopwords": len(stopwords),
            "stopwords" : str(stopwords),
            "plot": MetadataValue.md(md_content),
        }
    )

    return topstories[['by','url','descendants','score']]

## Top Stories - Top 10 Publishers

@asset(
        ins={"topstories": AssetIn("most_frequent_words")},
        group_name="hackernews"
)
def top_publishers(context: AssetExecutionContext, topstories: pd.DataFrame) -> None:

    grp = topstories.groupby(['by'])['by'].count().reset_index(name='counts')
    top10=grp.sort_values('counts', ascending=False)[:10]
    ticks = [*range(0,top10['counts'].max()+2)]

    # Make a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top10['by'], top10['counts'])
    plt.xticks(ticks=ticks)
    plt.title("Top 10 - Publishers")
    plt.tight_layout()

    # Convert the image to a saveable format
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())

    # Convert the image to Markdown to preview it within Dagster
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    # Attach the Markdown content as metadata to the asset
    context.add_output_metadata(
        metadata={
            "plot": MetadataValue.md(md_content),
        }
    )

## Top Stories - Top 10 Publishers

@asset(
        ins={"topstories": AssetIn("most_frequent_words")},
        group_name="hackernews"
)
def top_scores(context: AssetExecutionContext, topstories: pd.DataFrame) -> None:

    top10 = topstories[['url','score']].sort_values('score', ascending=False).copy()[0:10]
    top10['url'] = top10['url'].apply(lambda x: urlparse(x).netloc)

    ticks = [*range(0,top10['score'].max()+200,250)]

    # Make a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(top10['url'], top10['score'])
    plt.xticks(ticks=ticks)
    plt.title("Top 10 - Score")
    plt.tight_layout()

    # Convert the image to a saveable format
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    image_data = base64.b64encode(buffer.getvalue())

    # Convert the image to Markdown to preview it within Dagster
    md_content = f"![img](data:image/png;base64,{image_data.decode()})"

    # Attach the Markdown content as metadata to the asset
    context.add_output_metadata(
        metadata={
            "plot": MetadataValue.md(md_content),
        }
    )