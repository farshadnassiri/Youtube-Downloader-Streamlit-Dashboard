import streamlit as st
from pytubefix import YouTube

st.title("🎥 YouTube Downloader")
st.write("Paste a YouTube URL to view available video qualities.")

url = st.text_input(
    "Enter YouTube URL:",
    value="https://youtu.be/CMEWVn1uZpQ?si=T0u2tGhuwVEuWbz_"
)

if url:
    try:
        yt = YouTube(url)

        if st.button("Show Available Qualities"):
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            if not streams:
                st.warning("No downloadable streams found.")
            else:
                # استخراج اطلاعات خوانا برای کاربر
                options = [
                    f"{stream.resolution} ({round(stream.filesize / 1024 / 1024, 2)} MB)"
                    for stream in streams
                ]

                selected_quality = st.selectbox("Select video quality:", options)

                if st.button("Download"):
                    # پیدا کردن stream مربوط به گزینه انتخاب‌شده
                    index = options.index(selected_quality)
                    selected_stream = streams[index]

                    st.info("Downloading... Please wait ⏳")

                    # دانلود فایل
                    file_path = selected_stream.download()

                    st.success(f"✅ Download complete! Saved to: {file_path}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
