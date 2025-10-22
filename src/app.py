import streamlit as st
from pytubefix import YouTube
from main import YouTubeDownloader

st.title("🎥 YouTube Downloader")
st.write("Paste a YouTube URL to view available video qualities.")

url = st.text_input(
    "Enter YouTube URL:",
    value="https://youtu.be/7ZqWmAvLZEg?si=7j0bdWHk92HClDol" 
)

# اگر کاربر URL وارد کرده
if url:
    try:
        yt = YouTube(url)

        # فقط وقتی کاربر روی دکمه کلیک کرد
        if st.button("Show Available Qualities"):
            streams = yt.streams.filter(file_extension="mp4")

            if not streams:
                st.warning("No downloadable streams found.")
            else:
                st.session_state["streams"] = streams  # ذخیره برای بعداً

        # اگر استریم‌ها در حافظه هستند، نمایش انتخاب کیفیت
        if "streams" in st.session_state:
            streams = st.session_state["streams"]
            options = [
                f"{stream.resolution} ({round(stream.filesize / 1024 / 1024, 2)} MB)"
                for stream in streams
            ]
            selected_quality = st.selectbox("Select video quality:", options)

            if st.button("Download"):
                selected_res = selected_quality.split()[0]
                downloader = YouTubeDownloader(url, selected_res)

                with st.spinner("Downloading... Please wait ⏳"):
                    downloader.download()

                st.success("✅ Download complete!")

    except Exception as e:
        st.error(f"❌ Error: {e}")
