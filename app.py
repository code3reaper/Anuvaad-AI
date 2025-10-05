import streamlit as st
import tempfile
import os
from pathlib import Path
import time
from video_processor import VideoProcessor
from audio_processor import AudioProcessor
from translation_service import TranslationService
from dubbing_service import DubbingService
from sync_engine import SyncEngine
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
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')
        
        if not gemini_api_key:
            st.error("GEMINI_API_KEY environment variable not set")
            return None, None, None, None, None
        
        if not elevenlabs_api_key:
            st.error("ELEVENLABS_API_KEY environment variable not set")
            return None, None, None, None, None
        
        video_processor = VideoProcessor()
        audio_processor = AudioProcessor()
        translation_service = TranslationService(api_key=gemini_api_key)
        dubbing_service = DubbingService(api_key=elevenlabs_api_key)
        sync_engine = SyncEngine()
        return video_processor, audio_processor, translation_service, dubbing_service, sync_engine
    except Exception as e:
        st.error(f"Failed to initialize services: {str(e)}")
        return None, None, None, None, None

def main():
    st.title("🎬 AI Dubbing Studio")
    st.markdown("### Professional AI-powered video dubbing with perfect synchronization")
    
    # Initialize services
    services = initialize_services()
    if None in services:
        st.error("Failed to initialize application services. Please check API keys.")
        return
    
    video_processor, audio_processor, translation_service, dubbing_service, sync_engine = services
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Language selection
        source_lang = st.selectbox(
            "Source Language",
            ["en", "hi"],
            format_func=lambda x: "English" if x == "en" else "Hindi"
        )
        
        target_lang = st.selectbox(
            "Target Language", 
            ["hi", "en"],
            format_func=lambda x: "Hindi" if x == "hi" else "English"
        )
        
        # Voice settings
        st.subheader("Voice Settings")
        voice_stability = st.slider("Voice Stability", 0.0, 1.0, 0.75, 0.05)
        voice_clarity = st.slider("Voice Clarity", 0.0, 1.0, 0.75, 0.05)
        voice_style = st.slider("Voice Style", 0.0, 1.0, 0.0, 0.05)
        
        # Processing options
        st.subheader("Processing Options")
        preserve_background = st.checkbox("Preserve Background Audio", value=True)
        enhance_speech = st.checkbox("Enhance Speech Quality", value=True)
        
    # Main content area
    col1, col2 = st.columns([1, 1])
    
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
            video_info = video_processor.get_video_info(input_video_path)
            if video_info:
                st.info(f"Duration: {format_time(video_info['duration'])} | Resolution: {video_info['width']}x{video_info['height']} | FPS: {video_info['fps']:.1f}")
    
    with col2:
        st.header("Processing")
        
        if uploaded_file is not None and st.button("🚀 Start Dubbing", type="primary"):
            process_video(
                input_video_path, 
                source_lang, 
                target_lang,
                voice_stability,
                voice_clarity, 
                voice_style,
                preserve_background,
                enhance_speech,
                video_processor,
                audio_processor,
                translation_service,
                dubbing_service,
                sync_engine
            )

def process_video(input_path, source_lang, target_lang, stability, clarity, style, preserve_bg, enhance, 
                 video_proc, audio_proc, trans_svc, dub_svc, sync_eng):
    """Main video processing pipeline"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize variables for cleanup
    extracted_audio_path = None
    speech_audio = None
    background_audio = None
    dubbed_audio_path = None
    synced_audio_path = None
    final_audio_path = None
    
    try:
        # Stage 1: Audio Extraction
        status_text.text("🎵 Extracting audio from video...")
        progress_bar.progress(10)
        
        extracted_audio_path = video_proc.extract_audio(input_path)
        if not extracted_audio_path:
            st.error("Failed to extract audio from video")
            return
        
        # Stage 2: Audio Analysis and Separation
        status_text.text("🔍 Analyzing audio and separating speech from background...")
        progress_bar.progress(20)
        
        speech_audio, background_audio, timestamps = audio_proc.separate_audio_components(
            extracted_audio_path, preserve_background=preserve_bg
        )
        
        # Stage 3: Speech Recognition
        status_text.text("🗣️ Converting speech to text...")
        progress_bar.progress(35)
        
        transcript_data = audio_proc.speech_to_text(speech_audio, source_lang)
        if not transcript_data:
            st.error("Failed to transcribe speech")
            return
        
        st.subheader("Original Transcript")
        st.text_area("Detected Speech", transcript_data['text'], height=100)
        
        # Stage 4: Translation
        status_text.text("🌐 Translating text...")
        progress_bar.progress(50)
        
        translated_text = trans_svc.translate_text(
            transcript_data['text'], 
            source_lang, 
            target_lang
        )
        
        if not translated_text:
            st.error("Failed to translate text")
            return
            
        st.subheader("Translated Text")
        st.text_area("Translation", translated_text, height=100)
        
        # Stage 5: Voice Dubbing
        status_text.text("🎙️ Generating dubbed audio...")
        progress_bar.progress(65)
        
        dubbed_audio_path = dub_svc.generate_speech(
            translated_text,
            target_lang,
            stability=stability,
            clarity=clarity,
            style=style,
            enhance=enhance
        )
        
        if not dubbed_audio_path:
            st.error("Failed to generate dubbed audio")
            return
        
        # Stage 6: Audio Synchronization
        status_text.text("⚡ Synchronizing audio with video timing...")
        progress_bar.progress(80)
        
        synced_audio_path = sync_eng.synchronize_audio(
            dubbed_audio_path,
            transcript_data['segments'],
            extracted_audio_path
        )
        
        # Stage 7: Background Audio Mixing
        status_text.text("🎚️ Mixing dubbed speech with background audio...")
        progress_bar.progress(90)
        
        if preserve_bg and background_audio:
            final_audio_path = audio_proc.mix_audio_tracks(
                synced_audio_path,
                background_audio,
                speech_volume=1.0,
                background_volume=0.3
            )
        else:
            final_audio_path = synced_audio_path
        
        # Stage 8: Final Video Assembly
        status_text.text("🎬 Creating final dubbed video...")
        progress_bar.progress(95)
        
        output_video_path = video_proc.create_dubbed_video(
            input_path,
            final_audio_path
        )
        
        if not output_video_path:
            st.error("Failed to create final video")
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
            st.video(output_video_path)
        
        # Download button
        with open(output_video_path, 'rb') as f:
            st.download_button(
                label="📥 Download Dubbed Video",
                data=f.read(),
                file_name=f"dubbed_{int(time.time())}.mp4",
                mime="video/mp4",
                type="primary"
            )
        
        # Audio comparison
        st.subheader("Audio Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Original Audio**")
            st.audio(extracted_audio_path)
        
        with col2:
            st.write("**Dubbed Audio**")
            st.audio(final_audio_path)
            
    except Exception as e:
        st.error(f"Processing failed: {str(e)}")
        progress_bar.progress(0)
        status_text.text("❌ Processing failed")
    
    finally:
        # Cleanup temporary files
        cleanup_temp_files([
            extracted_audio_path,
            speech_audio,
            dubbed_audio_path,
            synced_audio_path,
            final_audio_path
        ])

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
