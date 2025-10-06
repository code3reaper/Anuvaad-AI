import streamlit as st
import tempfile
import os
from pathlib import Path
import time
from video_processor import VideoProcessor
from elevenlabs_dubbing import ElevenLabsDubbing
from utils import format_time, validate_video_file
import speech_recognition as sr
from elevenlabs import ElevenLabs
from google import genai
from pydub import AudioSegment

st.set_page_config(
    page_title="Anuvaad AI - Professional Video Dubbing",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], .main {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #0f172a;
    }
    
    .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .block-container {
        padding: 0 2rem !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    section[data-testid="stVerticalBlock"] > div {
        padding: 0 !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 4px solid transparent !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        background: 
            linear-gradient(135deg, rgba(30, 41, 59, 0.98), rgba(51, 65, 85, 0.98)) padding-box,
            linear-gradient(135deg, #60a5fa, #a78bfa, #ec4899) border-box !important;
        box-shadow: 
            0 0 60px rgba(96, 165, 250, 0.8),
            0 0 120px rgba(167, 139, 250, 0.6),
            0 20px 60px rgba(0, 0, 0, 0.7),
            inset 0 1px 0 rgba(96, 165, 250, 0.2) !important;
        position: relative !important;
    }
    
    .header {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.5rem 4rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0;
    }
    
    .logo {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    .hero {
        text-align: center;
        padding: 5rem 2rem 3rem 2rem;
        background: rgba(96, 165, 250, 0.05);
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        margin: 0;
    }
    
    .hero h1 {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero p {
        font-size: 1.5rem;
        color: #cbd5e1;
        font-weight: 300;
        max-width: 800px;
        margin: 0 auto 2rem auto;
    }
    
    .badge {
        display: inline-block;
        background: rgba(96, 165, 250, 0.2);
        color: #60a5fa;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .content-section {
        padding: 3rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    @media (max-width: 768px) {
        .content-section {
            padding: 2rem 1rem;
        }
        
        .header {
            padding: 1.5rem 2rem;
        }
        
        .block-container {
            padding: 0 1rem !important;
        }
    }
    
    .card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-box {
        background: rgba(96, 165, 250, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        background: rgba(96, 165, 250, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(96, 165, 250, 0.2);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        color: #94a3b8;
        line-height: 1.5;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.6);
    }
    
    .stSelectbox label {
        font-weight: 700 !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.8rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.95) !important;
        border: 2px solid rgba(96, 165, 250, 0.5) !important;
        color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: rgba(30, 41, 59, 0.95) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    .stSelectbox svg {
        fill: #60a5fa !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    .stSelectbox [aria-expanded="true"] svg {
        fill: #a78bfa !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    }
    
    .upload-zone {
        border: 2px dashed rgba(96, 165, 250, 0.4);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background: rgba(96, 165, 250, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: rgba(96, 165, 250, 0.6);
        background: rgba(96, 165, 250, 0.1);
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: #cbd5e1;
        margin: 1rem 0;
    }
    
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: #86efac;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 3rem;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    h5 {
        color: #e0e7ff !important;
        font-weight: 700 !important;
        margin-bottom: 0.8rem !important;
    }
    
    p {
        color: #cbd5e1;
    }
    
    .stVideo {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

def render_text_to_speech(elevenlabs_client):
    st.markdown("### 🗣️ Text to Speech")
    
    text_input = st.text_area(
        "Enter text to convert to speech",
        placeholder="Type or paste your text here...",
        height=150,
        key="tts_input"
    )
    
    voice_id = st.selectbox(
        "Select Voice",
        ["Rachel", "Adam", "Antoni", "Arnold", "Bella", "Domi", "Elli", "Josh", "Sam"],
        key="tts_voice"
    )
    
    voice_map = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Bella": "EXAVITQu4vr4xnSDxMaL",
        "Domi": "AZnzlk1XvdvUeBnXmlld",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Sam": "yoZ06aMxZJJ28mfd3POQ"
    }
    
    if st.button("🎵 Generate Speech", key="tts_btn", use_container_width=True):
        if not text_input.strip():
            st.error("Please enter some text first")
        else:
            try:
                with st.spinner("Generating speech..."):
                    audio = elevenlabs_client.generate(
                        text=text_input,
                        voice=voice_map[voice_id],
                        model="eleven_multilingual_v2"
                    )
                    
                    audio_bytes = b''.join(audio)
                    
                    st.audio(audio_bytes, format='audio/mpeg')
                    
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_bytes,
                        file_name=f"tts_{int(time.time())}.mp3",
                        mime="audio/mpeg",
                        key="tts_download"
                    )
                    
                    st.success("✅ Speech generated successfully!")
            except Exception as e:
                st.error(f"❌ Failed to generate speech: {str(e)}")

def render_speech_to_text():
    st.markdown("### 🎤 Speech to Text")
    
    uploaded_audio = st.file_uploader(
        "Upload audio file",
        type=['wav', 'mp3', 'ogg', 'flac', 'm4a'],
        key="stt_upload"
    )
    
    if uploaded_audio:
        st.audio(uploaded_audio)
    else:
        st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    
    if st.button("📝 Transcribe", key="stt_btn", use_container_width=True, disabled=uploaded_audio is None):
        if uploaded_audio:
            try:
                with st.spinner("Transcribing audio..."):
                    file_extension = uploaded_audio.name.split('.')[-1].lower()
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_input:
                        tmp_input.write(uploaded_audio.read())
                        input_path = tmp_input.name
                    
                    wav_path = tempfile.mktemp(suffix='.wav')
                    
                    try:
                        audio = AudioSegment.from_file(input_path, format=file_extension)
                        audio.export(wav_path, format='wav')
                    except Exception as e:
                        os.unlink(input_path)
                        raise Exception(f"Failed to convert audio: {str(e)}")
                    
                    recognizer = sr.Recognizer()
                    
                    try:
                        with sr.AudioFile(wav_path) as source:
                            audio_data = recognizer.record(source)
                            text = recognizer.recognize_google(audio_data)
                    finally:
                        os.unlink(input_path)
                        if os.path.exists(wav_path):
                            os.unlink(wav_path)
                    
                    st.markdown("##### 📄 Transcription:")
                    st.text_area("Result", value=text, height=150, key="stt_result")
                    
                    st.success("✅ Transcription completed!")
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio. Please try with clearer audio.")
            except Exception as e:
                st.error(f"❌ Transcription failed: {str(e)}")

def render_text_translation(gemini_client):
    st.markdown("### 🌐 Text Translation")
    
    source_text = st.text_area(
        "Enter text to translate",
        placeholder="Type or paste text here...",
        height=120,
        key="trans_input"
    )
    
    trans_col1, trans_col2 = st.columns(2)
    
    with trans_col1:
        from_lang = st.selectbox(
            "From",
            ["English", "Hindi", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean", "Chinese"],
            key="trans_from"
        )
    
    with trans_col2:
        to_lang = st.selectbox(
            "To",
            ["Hindi", "English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Korean", "Chinese"],
            key="trans_to"
        )
    
    if st.button("🔄 Translate", key="trans_btn", use_container_width=True):
        if not source_text.strip():
            st.error("Please enter some text to translate")
        elif from_lang == to_lang:
            st.error("Source and target languages must be different")
        else:
            try:
                with st.spinner("Translating..."):
                    prompt = f"Translate the following text from {from_lang} to {to_lang}. Only provide the translation, no explanations:\n\n{source_text}"
                    
                    response = gemini_client.models.generate_content(
                        model="gemini-2.0-flash-exp",
                        contents=prompt
                    )
                    translated_text = response.text
                    
                    st.markdown("##### 📝 Translation:")
                    st.text_area("Result", value=translated_text, height=120, key="trans_result")
                    
                    st.success(f"✅ Translated from {from_lang} to {to_lang}")
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")

@st.cache_resource
def initialize_services():
    try:
        elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        
        if not elevenlabs_api_key:
            st.error("🔑 ELEVENLABS_API_KEY environment variable not set")
            return None, None, None, None
        
        if not gemini_api_key:
            st.error("🔑 GEMINI_API_KEY environment variable not set")
            return None, None, None, None
        
        video_processor = VideoProcessor()
        dubbing_service = ElevenLabsDubbing(api_key=elevenlabs_api_key)
        elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        gemini_client = genai.Client(api_key=gemini_api_key)
        
        return video_processor, dubbing_service, elevenlabs_client, gemini_client
    except Exception as e:
        st.error(f"❌ Failed to initialize services: {str(e)}")
        return None, None, None, None

def main():
    st.markdown("""
        <div class="header">
            <span class="logo">🌐 Anuvaad AI</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="hero">
            <h1>Transform Content<br>Across Languages</h1>
            <p>AI-powered video dubbing, text-to-speech, speech-to-text, and translation</p>
            <span class="badge">✨ Powered by ElevenLabs & Google Gemini</span>
        </div>
    """, unsafe_allow_html=True)
    
    services = initialize_services()
    if None in services:
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.error("⚠️ Failed to initialize application services. Please check API keys.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    video_processor, dubbing_service, elevenlabs_client, gemini_client = services
    
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    with st.container(border=True, key="main_dubbing"):
        st.markdown('<h2 style="text-align: center; margin: 0 0 1.5rem 0;">🎬 Video Dubbing - Main Feature</h2>', unsafe_allow_html=True)
        
        input_video_path = None
        
        st.markdown("#### 📤 Upload Video")
        
        uploaded_file = st.file_uploader(
            "Choose your video file",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Supported formats: MP4, AVI, MOV, MKV | Max size: 100MB"
        )
        
        if uploaded_file is not None:
            if not validate_video_file(uploaded_file):
                st.error("❌ Invalid video file or file too large (max 100MB)")
                st.stop()
                
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                input_video_path = tmp_file.name
            
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                st.markdown("#### 🎥 Preview")
                st.video(input_video_path)
            
            with col2:
                st.markdown("#### ⚙️ Configuration")
                
                st.markdown("##### 🌍 Source Language")
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
                
                st.markdown("##### 🎯 Target Language")
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
                
                lang_display = {
                    "en": "English", "hi": "Hindi", "es": "Spanish", 
                    "fr": "French", "de": "German", "it": "Italian",
                    "pt": "Portuguese", "ja": "Japanese", 
                    "ko": "Korean", "zh": "Chinese"
                }
                
                st.markdown(f"""
                    <div class="info-box">
                        <strong>Translation Path:</strong><br>
                        {lang_display[source_lang]} → {lang_display[target_lang]}
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("🎙️ Start Dubbing", type="primary", use_container_width=True):
                    process_video_with_elevenlabs(
                        input_video_path, 
                        source_lang, 
                        target_lang,
                        video_processor,
                        dubbing_service
                    )
        else:
            st.markdown("""
                <div class="info-box">
                    <strong>📋 Instructions:</strong><br>
                    1. Upload your video file<br>
                    2. Select source language<br>
                    3. Choose target language<br>
                    4. Click Start Dubbing
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h2 style="text-align: center; margin: 2rem 0;">Additional Features</h2>', unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")
    
    with feat_col1:
        render_text_to_speech(elevenlabs_client)
    
    with feat_col2:
        render_speech_to_text()
    
    with feat_col3:
        render_text_translation(gemini_client)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="footer">
            <p>© 2025 Anuvaad AI - Powered by ElevenLabs Technology</p>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;">Breaking language barriers with artificial intelligence</p>
        </div>
    """, unsafe_allow_html=True)

def process_video_with_elevenlabs(input_path, source_lang, target_lang, video_proc, dub_svc):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🔄 Processing</div>', unsafe_allow_html=True)
    
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
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        progress_bar.progress(100)
        status_text.markdown("**✅ Dubbing completed!**")
        time.sleep(0.5)
        
        st.balloons()
        st.success("🎉 Your video is ready!")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📹 Original")
            st.video(input_path)
        
        with col2:
            st.markdown("##### 🎬 Dubbed")
            st.video(dubbed_video_path)
        
        st.markdown("---")
        
        with open(dubbed_video_path, 'rb') as f:
            st.download_button(
                label="📥 Download Dubbed Video",
                data=f.read(),
                file_name=f"anuvaad_ai_{source_lang}_to_{target_lang}_{int(time.time())}.mp4",
                mime="video/mp4",
                type="primary",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        progress_bar.progress(0)
        status_text.markdown("**❌ Processing failed**")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
