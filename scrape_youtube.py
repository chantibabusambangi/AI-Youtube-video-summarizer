#chanti babu sambangi
import sys
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def extract_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_tag = soup.find("meta", property="og:title")
    title = title_tag['content'] if title_tag else "Unknown Title"

    # Extract channel name more robustly
    channel_tag = soup.find("link", itemprop="name")
    channel = channel_tag['content'] if channel_tag and 'content' in channel_tag.attrs else "Unknown Channel"

    return title, channel

def download_thumbnail(video_id):
    image_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    img_data = requests.get(image_url).content
    with open('thumbnail.jpg', 'wb') as handler:
        handler.write(img_data)
def get_transcript(video_id):
    transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'ko'])
    transcript_full = ' '.join([i['text'] for i in transcript_raw])
    return transcript_full
