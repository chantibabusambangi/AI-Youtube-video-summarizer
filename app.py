import streamlit as st
from scrape_youtube import extract_video_id, get_transcript, extract_metadata, download_thumbnail
from summarize_text1 import summarize_text
import os

def main():
    title_text = "YouTube AI Video Summarizer"
    image_url = "https://i.pinimg.com/originals/3a/36/20/3a36206f35352b4230d5fc9f17fcea92.png"
    html_code = f"""
    <div style="display: flex; align-items: center; margin-bottom: 30px;">
        <img src="{image_url}" alt="Tiny Image" style="width: 50px; height: 50px; margin-right: 15px;">
        <h3 style="font-size: 45px;">{title_text}</h3>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    # Function to get thumbnail from URL
    def get_thumbnail_from_url(url):
        video_id = extract_video_id(url)
        download_thumbnail(video_id)
    
    # Function to get transcript from URL
    def get_transcript_from_url(url):
        video_id = extract_video_id(url)
        transcript = get_transcript(video_id)
        return transcript

    # Function to summarize text
    def summarize_transcript(transcript, lang):
        summary = summarize_text(transcript, lang=lang)
        return summary

    st.subheader("Enter YouTube URL Now:")
    st.write("Paste a YouTube link to summarize its content (must have a transcript available) alright!")
    url = st.text_input("URL")
    language = st.radio("Select language to output:", ('English', 'Spanish', 'Korean'))
    if st.button("Summarize"):
        if url:
            title, channel = extract_metadata(url)
            st.subheader("Title:")
            st.write(title)
            st.subheader("Channel:")
            st.write(channel)
            
            get_thumbnail_from_url(url)
            st.image(os.path.join(os.getcwd(), "thumbnail.jpg"), caption='Thumbnail', use_column_width=True)
            
            transcript = get_transcript_from_url(url)
            summary = summarize_transcript(transcript, language)
            st.subheader("Video Summary:")
            st.write(summary)
        else:
            st.warning("Please enter a YouTube URL.")
if __name__ == "__main__":
    main()
