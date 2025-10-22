from pytubefix import YouTube
import streamlit as st

st.title("🎥 YouTube Downloader")
st.write("Paste a YouTube URL to view and download available video qualities.")

# --- ورودی لینک ---
url = st.text_input("Enter YouTube URL:")

# --- مدیریت وضعیت ---
if "yt" not in st.session_state:
    st.session_state.yt = None
if "streams" not in st.session_state:
    st.session_state.streams = None
if "last_url" not in st.session_state:
    st.session_state.last_url = None
if "selected_res" not in st.session_state:
    st.session_state.selected_res = None

# --- وقتی لینک جدید وارد شد، state ریست بشه ---
if url != st.session_state.last_url:
    st.session_state.yt = None
    st.session_state.streams = None
    st.session_state.selected_res = None
    st.session_state.last_url = url

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

# --- نمایش کیفیت‌ها در صورت وجود ---
if st.session_state.streams:
    options = [
        f"{stream.resolution} ({round(stream.filesize / 1024 / 1024, 2)} MB)"
        for stream in st.session_state.streams
    ]

    selected_res = st.selectbox(
        "Select video quality:",
        options,
        index=options.index(st.session_state.selected_res)
        if st.session_state.selected_res in options
        else 0
    )
    st.session_state.selected_res = selected_res
    st.success(f"✅ کیفیت انتخاب‌شده: {selected_res}")

    # --- دکمه دانلود ---
    if st.button("⬇️ دانلود ویدیو"):
        try:
            res = selected_res.split(" ")[0]  # مثلاً '720p'
            stream = next(
                (s for s in st.session_state.streams if s.resolution == res), None
            )

            if stream:
                st.info("📥 در حال دانلود ویدیو، لطفاً صبر کنید...")
                file_path = stream.download()
                st.success(f"✅ دانلود انجام شد!\n📂 مسیر فایل: `{file_path}`")
            else:
                st.error("❌ کیفیت مورد نظر یافت نشد.")
        except Exception as e:
            st.error(f"⚠️ خطا در دانلود ویدیو: {e}")
