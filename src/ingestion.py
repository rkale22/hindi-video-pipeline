import os
import requests
from dotenv import load_dotenv
import csv

# Load environment variables from .env
load_dotenv()  # This reads .env file and loads keys into environment

API_KEY = os.getenv("YT_API_KEY")


BASE_URL = "https://youtube.googleapis.com/youtube/v3/search"

def fetch_youtube_metadata(query="Hindi Language Lessons", max_results=5):
    """
    Fetch video metadata from YouTube Data API based on a query.
    Returns a list of dictionaries with videoId, title, description, publishedAt, channelTitle.
    """
    # Construct request parameters
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "type": "video",
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # Throw an error if request fails

    data = response.json()

    items = []
    for item in data.get("items", []):
        snippet = item["snippet"]
        video_id = item["id"].get("videoId")  # "videoId" might be absent if it's a channel or playlist
        if not video_id:
            continue  # skip if it's not a real video
        items.append({
            "videoId": video_id,
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "publishedAt": snippet.get("publishedAt"),
            "channelTitle": snippet.get("channelTitle")
        })

    return items


def save_metadata_to_csv(metadata_list, csv_filename="video_metadata.csv"):
    """
    Save the list of metadata dicts to a CSV file.
    """
    if not metadata_list:
        print("No data to save.")
        return

    # Define CSV column names (keys in the dict)
    fieldnames = ["videoId", "title", "description", "publishedAt", "channelTitle"]

    # Open CSV and write data
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in metadata_list:
            writer.writerow(row)

    print(f"Saved {len(metadata_list)} records to {csv_filename}")

if __name__ == "__main__":
    # Quick test
    results = fetch_youtube_metadata("Hindi grammar basics", max_results=3)
    print("Fetched results:", results)
    save_metadata_to_csv(results, "video_metadata.csv")
