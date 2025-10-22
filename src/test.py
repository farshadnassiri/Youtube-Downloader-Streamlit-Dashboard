from pytubefix import YouTube
import streamlit as st

st.title("🎥 YouTube Downloader")
st.write("Paste a YouTube URL to view available video qualities.")

# --- ورودی لینک ---
url = st.text_input("Enter YouTube URL:")

# --- بررسی و ذخیره وضعیت ---
if "yt" not in st.session_state:
    st.session_state.yt = None
if "streams" not in st.session_state:
    st.session_state.streams = None

# --- دکمه دریافت اطلاعات ---
if st.button("دریافت اطلاعات") and url:
    try:
        yt = YouTube(url)
        st.session_state.yt = yt
        st.success(f"🎬 عنوان ویدیو: {yt.title}")
        streams = yt.streams.filter(file_extension="mp4")
        if streams:
            st.session_state.streams = streams
        else:
            st.warning("⚠️ No downloadable streams found.")
    except Exception as e:
        st.error(f"❌ خطا در خواندن ویدیو: {e}")
if url =="":
       st.session_state.yt = None
       st.session_state.streams = None


# --- نمایش کیفیت‌ها در صورت وجود ---
if st.session_state.streams:
    options = [
        f"{stream.resolution} ({round(stream.filesize / 1024 / 1024, 2)} MB)"
        for stream in st.session_state.streams
    ]
    selected_res = st.selectbox("Select video quality:", options)
    st.success(f"✅ کیفیت انتخاب‌شده: {selected_res}")
