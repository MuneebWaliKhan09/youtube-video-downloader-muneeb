import streamlit as st
from pytube import YouTube
import os

def sanitize_filename(title):
    # Remove invalid characters from the title
    invalid_chars = set(r'\/:*?"<>|')
    return ''.join(char if char not in invalid_chars else '_' for char in title)

def download_youtube_video(url, resolution='720p'):
    try:
        # Create a YouTube object
        video = YouTube(url)

        # Get streams with both video and audio
        streams = video.streams.filter(progressive=True, file_extension="mp4", type="video")

        # Get the selected stream based on resolution
        stream = streams.filter(res=resolution, file_extension="mp4", audio_codec="mp4a.40.2").first()

        if stream is None:
            return False, f"No {resolution} stream found for the video."

        # Sanitize the video title for a valid filename
        filename = sanitize_filename(video.title) + ".mp4"

        # Download the video directly to the user's DOWNLOADS folder
        downloads_path = os.path.expanduser("~/Downloads")
        filepath = os.path.join(downloads_path, filename)
        stream.download(filepath)

        return True, filename
    except Exception as e:
        return False, f"Error: {str(e)}"

def embed_youtube_video(url):
    # Create an HTML iframe to embed the YouTube video
    html_code = f'<iframe width="500" height="315" src="{url}" frameborder="0" allowfullscreen></iframe>'
    return html_code

def main():
    st.title("YouTube Video Downloader and Viewer by Muneeb")

    # Input for YouTube video URL
    url = st.text_input("Enter YouTube video URL:")

    # Display YouTube video
    if url:
        try:
            video = YouTube(url)
            # Get the stream with the highest resolution
            stream = video.streams.get_highest_resolution()
            video_url = stream.url
            st.subheader("YouTube Video:")
            st.write(embed_youtube_video(video_url), unsafe_allow_html=True)

            # Resolution selection
            resolution_options = ['720p', '360p', '240p']
            resolution = st.selectbox("Select resolution:", resolution_options)

            # Download button
            if st.button("Download"):
                success, filename = download_youtube_video(url, resolution)
                if success:
                    st.success("Download successful!")
                    # Provide a download link
                    st.markdown(f"Please Check the Downloads TAB on your PC({filename})", unsafe_allow_html=True)
                else:
                    st.error(filename)

        except Exception as e:
            st.error(f"Error loading video: {str(e)}")

if __name__ == "__main__":
    main()
