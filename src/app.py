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
if "selected_itag" not in st.session_state:
    st.session_state.selected_itag = None

# --- اگر لینک جدید وارد شد، state ریست بشه ---
if url != st.session_state.last_url:
    st.session_state.yt = None
    st.session_state.streams = None
    st.session_state.selected_itag = None
    st.session_state.last_url = url

# --- دکمه دریافت اطلاعات ---
if st.button("دریافت اطلاعات") and url:
    try:
        yt = YouTube(url)
        st.session_state.yt = yt
        st.success(f"🎬 عنوان ویدیو: {yt.title}")

        # فقط استریم‌های MP4 و progressive (ویدیو + صدا)
        streams = yt.streams.filter(file_extension="mp4")
        if streams:
            st.session_state.streams = streams
        else:
            st.warning("⚠️ No downloadable streams found.")
    except Exception as e:
        st.error(f"❌ خطا در خواندن ویدیو: {e}")

# --- نمایش کیفیت‌ها در صورت وجود ---
if st.session_state.streams:
    # دیکشنری از توضیحات برای نمایش به کاربر -> itag برای شناسایی دقیق
    options = {
        f"{s.resolution} | {s.fps}fps | {s.mime_type} | {round(s.filesize / 1024 / 1024, 2)} MB": s.itag
        for s in st.session_state.streams
    }

    # لیست متن‌ها برای انتخاب در UI
    option_labels = list(options.keys())

    selected_label = st.selectbox(
        "Select video quality:",
        option_labels,
        index=option_labels.index(
            next(
                (k for k, v in options.items() if v == st.session_state.selected_itag),
                option_labels[0],
            )
        )
        if st.session_state.selected_itag
        else 0,
    )

    # ذخیره itag انتخاب‌شده
    st.session_state.selected_itag = options[selected_label]
    st.success(f"✅ کیفیت انتخاب‌شده: {selected_label}")

    # --- دکمه دانلود ---
    if st.button("⬇️ دانلود ویدیو"):
        try:
            stream = st.session_state.yt.streams.get_by_itag(
                st.session_state.selected_itag
            )
            st.info("📥 در حال دانلود ویدیو، لطفاً صبر کنید...")
            file_path = stream.download()
            st.success(f"✅ دانلود انجام شد!\n📂 مسیر فایل: `{file_path}`")
        except Exception as e:
            st.error(f"⚠️ خطا در دانلود ویدیو: {e}")
