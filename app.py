import streamlit as st
import tempfile
import os
from pathlib import Path
import time
from video_processor import VideoProcessor
from elevenlabs_dubbing import ElevenLabsDubbing
from utils import format_time, validate_video_file

st.set_page_config(
    page_title="AI Dubbing Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    h1 {
        color: #1e293b;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    .upload-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stSelectbox label {
        font-weight: 600;
        color: #1e293b;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_services():
    try:
        elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')
        
        if not elevenlabs_api_key:
            st.error("🔑 ELEVENLABS_API_KEY environment variable not set")
            return None, None
        
        video_processor = VideoProcessor()
        dubbing_service = ElevenLabsDubbing(api_key=elevenlabs_api_key)
        
        return video_processor, dubbing_service
    except Exception as e:
        st.error(f"❌ Failed to initialize services: {str(e)}")
        return None, None

def main():
    st.markdown("<h1>🎬 AI Dubbing Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Transform your videos into any language with AI-powered voice dubbing</p>", unsafe_allow_html=True)
    
    services = initialize_services()
    if None in services:
        st.error("⚠️ Failed to initialize application services. Please check API keys.")
        return
    
    video_processor, dubbing_service = services
    
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")
        
        st.markdown("#### 🌍 Source Language")
        source_lang = st.selectbox(
            "From",
            ["en", "hi", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            format_func=lambda x: {
                "en": "🇬🇧 English", "hi": "🇮🇳 Hindi", "es": "🇪🇸 Spanish", 
                "fr": "🇫🇷 French", "de": "🇩🇪 German", "it": "🇮🇹 Italian",
                "pt": "🇵🇹 Portuguese", "ja": "🇯🇵 Japanese", 
                "ko": "🇰🇷 Korean", "zh": "🇨🇳 Chinese"
            }.get(x, x),
            label_visibility="collapsed"
        )
        
        st.markdown("#### 🎯 Target Language")
        target_lang = st.selectbox(
            "To",
            ["hi", "en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            format_func=lambda x: {
                "en": "🇬🇧 English", "hi": "🇮🇳 Hindi", "es": "🇪🇸 Spanish", 
                "fr": "🇫🇷 French", "de": "🇩🇪 German", "it": "🇮🇹 Italian",
                "pt": "🇵🇹 Portuguese", "ja": "🇯🇵 Japanese", 
                "ko": "🇰🇷 Korean", "zh": "🇨🇳 Chinese"
            }.get(x, x),
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 🚀 Features")
        st.markdown("""
        - ✨ AI-powered voice cloning
        - 🎭 Emotion preservation
        - ⚡ Fast processing
        - 🎬 Professional quality
        - 🌐 32+ languages
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Powered By")
        st.markdown("**ElevenLabs AI**")
        st.caption("Industry-leading voice technology")
        
    col1, col2 = st.columns([1, 1], gap="large")
    
    input_video_path = None
    
    with col1:
        st.markdown("### 📤 Upload Your Video")
        
        uploaded_file = st.file_uploader(
            "Drag and drop your video here",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="📹 Supported formats: MP4, AVI, MOV, MKV | Max size: 100MB",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            if not validate_video_file(uploaded_file):
                st.error("❌ Invalid video file or file too large (max 100MB)")
                return
                
            st.success(f"✅ {uploaded_file.name}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                input_video_path = tmp_file.name
            
            st.markdown("#### 🎥 Original Video")
            st.video(input_video_path)
            
            if video_processor:
                video_info = video_processor.get_video_info(input_video_path)
                if video_info:
                    info_col1, info_col2, info_col3 = st.columns(3)
                    with info_col1:
                        st.markdown(f"<div class='stat-box'><b>⏱️ Duration</b><br>{format_time(video_info['duration'])}</div>", unsafe_allow_html=True)
                    with info_col2:
                        st.markdown(f"<div class='stat-box'><b>📐 Resolution</b><br>{video_info['width']}x{video_info['height']}</div>", unsafe_allow_html=True)
                    with info_col3:
                        st.markdown(f"<div class='stat-box'><b>🎞️ FPS</b><br>{video_info['fps']:.1f}</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Upload a video file to get started")
    
    with col2:
        st.markdown("### 🎬 Processing Center")
        
        if uploaded_file is None:
            st.markdown("""
            <div class='feature-card'>
                <h4>🎯 How it works</h4>
                <ol>
                    <li><b>Upload</b> your video file</li>
                    <li><b>Select</b> source and target languages</li>
                    <li><b>Click</b> Start Dubbing</li>
                    <li><b>Download</b> your dubbed video</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='feature-card'>
                <h4>✨ AI Technology</h4>
                <p>Our AI preserves the original speaker's emotion, tone, and timing while translating to your chosen language.</p>
            </div>
            """, unsafe_allow_html=True)
        
        if uploaded_file is not None and input_video_path is not None:
            st.markdown("#### 🚀 Ready to Process")
            
            lang_display = {
                "en": "English", "hi": "Hindi", "es": "Spanish", 
                "fr": "French", "de": "German", "it": "Italian",
                "pt": "Portuguese", "ja": "Japanese", 
                "ko": "Korean", "zh": "Chinese"
            }
            
            st.info(f"📍 {lang_display[source_lang]} → {lang_display[target_lang]}")
            
            if st.button("🎙️ Start Dubbing", type="primary", use_container_width=True):
                process_video_with_elevenlabs(
                    input_video_path, 
                    source_lang, 
                    target_lang,
                    video_processor,
                    dubbing_service
                )

def process_video_with_elevenlabs(input_path, source_lang, target_lang, video_proc, dub_svc):
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Processing Your Video")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
    try:
        status_text.markdown("**📤 Uploading to ElevenLabs...**")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        status_text.markdown("**🗣️ Transcribing speech...**")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.markdown(f"**🌐 Translating {source_lang.upper()} → {target_lang.upper()}...**")
        progress_bar.progress(40)
        
        status_text.markdown("**🎙️ Generating AI voice...**")
        progress_bar.progress(50)
        
        def progress_callback(message, percent):
            status_text.markdown(f"**{message}**")
            progress_bar.progress(percent)
        
        dubbed_video_path = dub_svc.dub_video_complete(
            input_path,
            source_lang,
            target_lang,
            progress_callback=progress_callback
        )
        
        if not dubbed_video_path:
            st.error("❌ Failed to dub video. Please check your ElevenLabs API key and quota.")
            st.info("🔗 Visit https://elevenlabs.io/ to check your account status")
            return
        
        progress_bar.progress(100)
        status_text.markdown("**✅ Dubbing completed successfully!**")
        time.sleep(1)
        
        st.balloons()
        st.success("🎉 Your video is ready!")
        
        st.markdown("---")
        st.markdown("### 📺 Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📹 Original")
            st.video(input_path)
        
        with col2:
            st.markdown("#### 🎬 Dubbed")
            st.video(dubbed_video_path)
        
        st.markdown("---")
        
        with open(dubbed_video_path, 'rb') as f:
            st.download_button(
                label="📥 Download Dubbed Video",
                data=f.read(),
                file_name=f"dubbed_{source_lang}_to_{target_lang}_{int(time.time())}.mp4",
                mime="video/mp4",
                type="primary",
                use_container_width=True
            )
            
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        progress_bar.progress(0)
        status_text.markdown("**❌ Processing failed**")

if __name__ == "__main__":
    main()
