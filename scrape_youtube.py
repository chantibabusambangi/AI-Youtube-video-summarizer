#chanti babu sambangi
import sys
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import os

# Load API key from environment variable (secure)
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")

# Set up proxy using your key
proxies = {
    "http": f"http://scraperapi:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001",
    "https": f"http://scraperapi:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001"
}

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            proxies=proxies,
            languages=['en']
        )
        return " ".join([t['text'] for t in transcript])
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "Transcript not found for this video."
    except Exception as e:
        return f"[Error fetching transcript] {e}"




def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def extract_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string.strip()

    channel_tag = soup.find("meta", itemprop="channelId")
    if channel_tag and channel_tag.get("content"):
        channel = channel_tag["content"]
    else:
        channel = "Unknown Channel"

    return title, channel


def download_thumbnail(video_id):
    image_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    img_data = requests.get(image_url).content
    with open('thumbnail.jpg', 'wb') as handler:
        handler.write(img_data)
'''def get_transcript(video_id):
    transcript_raw = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'ko'])
    transcript_full = ' '.join([i['text'] for i in transcript_raw])
    return transcript_full
'''
