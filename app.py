import streamlit as st
import tempfile
import os
from pathlib import Path
import time
from video_processor import VideoProcessor
from elevenlabs_dubbing import ElevenLabsDubbing
from utils import format_time, validate_video_file

# Set page config
st.set_page_config(
    page_title="AI Dubbing Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with API keys"""
    try:
        elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')
        
        if not elevenlabs_api_key:
            st.error("ELEVENLABS_API_KEY environment variable not set")
            return None, None
        
        video_processor = VideoProcessor()
        dubbing_service = ElevenLabsDubbing(api_key=elevenlabs_api_key)
        
        return video_processor, dubbing_service
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        return None, None

def main():
    st.title("🎬 AI Dubbing Studio")
    st.markdown("### Professional AI-powered video dubbing with perfect synchronization")
    
    # Initialize services
    services = initialize_services()
    if None in services:
        st.error("Failed to initialize application services. Please check API keys.")
        return
    
    video_processor, dubbing_service = services
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Language selection
        st.subheader("🌍 Languages")
        source_lang = st.selectbox(
            "Source Language",
            ["en", "hi", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            format_func=lambda x: {
                "en": "English", "hi": "Hindi", "es": "Spanish", 
                "fr": "French", "de": "German", "it": "Italian",
                "pt": "Portuguese", "ja": "Japanese", 
                "ko": "Korean", "zh": "Chinese"
            }.get(x, x)
        )
        
        target_lang = st.selectbox(
            "Target Language", 
            ["hi", "en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh"],
            format_func=lambda x: {
                "en": "English", "hi": "Hindi", "es": "Spanish", 
                "fr": "French", "de": "German", "it": "Italian",
                "pt": "Portuguese", "ja": "Japanese", 
                "ko": "Korean", "zh": "Chinese"
            }.get(x, x)
        )
        
        st.info("🚀 Powered by ElevenLabs AI Dubbing")
        
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    input_video_path = None
    
    with col1:
        st.header("Upload Video")
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Supported formats: MP4, AVI, MOV, MKV (max 10 minutes)"
        )
        
        if uploaded_file is not None:
            # Validate file
            if not validate_video_file(uploaded_file):
                st.error("Invalid video file or file too large (max 100MB)")
                return
                
            st.success(f"Uploaded: {uploaded_file.name}")
            
            # Save uploaded file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                input_video_path = tmp_file.name
            
            # Display original video
            st.subheader("Original Video")
            st.video(input_video_path)
            
            # Get video info
            if video_processor:
                video_info = video_processor.get_video_info(input_video_path)
                if video_info:
                    st.info(f"Duration: {format_time(video_info['duration'])} | Resolution: {video_info['width']}x{video_info['height']} | FPS: {video_info['fps']:.1f}")
    
    with col2:
        st.header("Processing")
        
        if uploaded_file is not None and input_video_path is not None and st.button("🚀 Start Dubbing", type="primary"):
            process_video_with_elevenlabs(
                input_video_path, 
                source_lang, 
                target_lang,
                video_processor,
                dubbing_service
            )

def process_video_with_elevenlabs(input_path, source_lang, target_lang, video_proc, dub_svc):
    """Process video using ElevenLabs dubbing API"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Stage 1: Upload to ElevenLabs
        status_text.text("📤 Uploading video to ElevenLabs...")
        progress_bar.progress(10)
        
        # Stage 2: Transcribing (shown to user, but happening on ElevenLabs)
        status_text.text("🗣️ Transcribing speech...")
        progress_bar.progress(25)
        time.sleep(1)  # Brief pause for UI
        
        # Stage 3: Translating (shown to user, but happening on ElevenLabs)
        status_text.text(f"🌐 Translating from {source_lang.upper()} to {target_lang.upper()}...")
        progress_bar.progress(40)
        
        # Stage 4: AI Dubbing (this is where the actual API call happens)
        status_text.text("🎙️ Generating AI voice dubbing...")
        progress_bar.progress(50)
        
        def progress_callback(message, percent):
            status_text.text(message)
            progress_bar.progress(percent)
        
        # Call ElevenLabs dubbing API (this does everything on their servers)
        dubbed_video_path = dub_svc.dub_video_complete(
            input_path,
            source_lang,
            target_lang,
            progress_callback=progress_callback
        )
        
        if not dubbed_video_path:
            st.error("❌ Failed to dub video. Please check your ElevenLabs API key and quota.")
            st.info("Visit https://elevenlabs.io/ to check your account status")
            return
        
        # Complete
        progress_bar.progress(100)
        status_text.text("✅ Dubbing completed successfully!")
        
        # Display results
        st.success("🎉 Video dubbing completed!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Video")
            st.video(input_path)
        
        with col2:
            st.subheader("Dubbed Video")
            st.video(dubbed_video_path)
        
        # Download button
        with open(dubbed_video_path, 'rb') as f:
            st.download_button(
                label="📥 Download Dubbed Video",
                data=f.read(),
                file_name=f"dubbed_{source_lang}_to_{target_lang}_{int(time.time())}.mp4",
                mime="video/mp4",
                type="primary"
            )
            
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Processing failed")

def cleanup_temp_files(file_paths):
    """Clean up temporary files"""
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except:
                pass

if __name__ == "__main__":
    main()
