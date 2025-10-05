import os
import tempfile
import whisper
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
import librosa
import soundfile as sf
from typing import Tuple, Optional, List, Dict

class AudioProcessor:
    """Handles audio processing, separation, and speech recognition"""
    
    def __init__(self):
        """Initialize audio processor with Whisper model"""
        self.whisper_model = whisper.load_model("base")
        
    def separate_audio_components(self, audio_path: str, preserve_background: bool = True) -> Tuple[str, Optional[str], List]:
        """
        Separate speech from background audio using advanced techniques
        Returns: (speech_audio_path, background_audio_path, timestamps)
        """
        try:
            # Load audio with pydub
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to mono for processing
            mono_audio = audio.set_channels(1)
            
            # Detect speech segments using silence detection
            speech_segments = detect_nonsilent(
                mono_audio,
                min_silence_len=100,  # 100ms minimum silence
                silence_thresh=mono_audio.dBFS - 16,  # 16dB below average
                seek_step=10
            )
            
            # Create speech-only audio
            speech_audio = AudioSegment.empty()
            silence_audio = AudioSegment.empty()
            timestamps = []
            
            last_end = 0
            for start_ms, end_ms in speech_segments:
                # Add silence before speech if exists
                if start_ms > last_end:
                    silence_duration = start_ms - last_end
                    silence_audio += AudioSegment.silent(duration=silence_duration)
                    speech_audio += AudioSegment.silent(duration=silence_duration)
                
                # Add speech segment
                speech_segment = mono_audio[start_ms:end_ms]
                speech_audio += speech_segment
                
                # Store timestamp info
                timestamps.append({
                    'start': start_ms / 1000.0,
                    'end': end_ms / 1000.0,
                    'duration': (end_ms - start_ms) / 1000.0
                })
                
                last_end = end_ms
            
            # Add final silence if needed
            if last_end < len(mono_audio):
                silence_duration = len(mono_audio) - last_end
                speech_audio += AudioSegment.silent(duration=silence_duration)
            
            # Save speech audio
            speech_path = tempfile.mktemp(suffix='.wav')
            speech_audio.export(speech_path, format='wav')
            
            background_path = None
            if preserve_background:
                # Create background audio by inverting speech segments
                background_audio = mono_audio.overlay(speech_audio.invert_phase())
                background_path = tempfile.mktemp(suffix='.wav')
                background_audio.export(background_path, format='wav')
            
            return speech_path, background_path, timestamps
            
        except Exception as e:
            print(f"Error in audio separation: {e}")
            # Fallback: return original audio as speech
            return audio_path, None, []
    
    def speech_to_text(self, audio_path: str, language: str) -> Optional[Dict]:
        """
        Convert speech to text with detailed timing information
        """
        try:
            # Set language code for Whisper
            lang_code = "en" if language == "en" else "hi"
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(
                audio_path,
                language=lang_code,
                word_timestamps=True,
                verbose=False
            )
            
            # Extract segments with timing
            segments = []
            for segment in result.get('segments', []):
                segments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'].strip(),
                    'words': segment.get('words', [])
                })
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', lang_code),
                'segments': segments
            }
            
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def enhance_audio_quality(self, audio_path: str) -> str:
        """
        Enhance audio quality through noise reduction and normalization
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Normalize audio
            normalized = audio.normalize()
            
            # Apply basic noise reduction by removing very quiet parts
            # This is a simple approach - more sophisticated methods would use spectral subtraction
            threshold = normalized.dBFS - 20
            enhanced = normalized.compress_dynamic_range(
                threshold=threshold,
                ratio=4.0,
                attack=5.0,
                release=50.0
            )
            
            # Export enhanced audio
            enhanced_path = tempfile.mktemp(suffix='.wav')
            enhanced.export(enhanced_path, format='wav')
            
            return enhanced_path
            
        except Exception as e:
            print(f"Error in audio enhancement: {e}")
            return audio_path
    
    def mix_audio_tracks(self, speech_path: str, background_path: str, 
                        speech_volume: float = 1.0, background_volume: float = 0.3) -> str:
        """
        Mix speech and background audio with specified volume levels
        """
        try:
            # Load audio files
            speech = AudioSegment.from_file(speech_path)
            background = AudioSegment.from_file(background_path)
            
            # Adjust volumes
            speech = speech + (20 * np.log10(speech_volume))  # Convert to dB
            background = background + (20 * np.log10(background_volume))
            
            # Ensure both tracks have the same length
            max_length = max(len(speech), len(background))
            
            if len(speech) < max_length:
                speech = speech + AudioSegment.silent(duration=max_length - len(speech))
            
            if len(background) < max_length:
                background = background + AudioSegment.silent(duration=max_length - len(background))
            
            # Mix the tracks
            mixed = speech.overlay(background)
            
            # Export mixed audio
            mixed_path = tempfile.mktemp(suffix='.wav')
            mixed.export(mixed_path, format='wav')
            
            return mixed_path
            
        except Exception as e:
            print(f"Error in audio mixing: {e}")
            return speech_path
    
    def analyze_audio_gaps(self, audio_path: str) -> List[Dict]:
        """
        Analyze gaps and pauses in audio for better synchronization
        """
        try:
            # Load audio
            audio = AudioSegment.from_file(audio_path)
            
            # Detect silent segments
            silence_segments = []
            silent_parts = split_on_silence(
                audio,
                min_silence_len=200,  # 200ms minimum silence
                silence_thresh=audio.dBFS - 14,
                keep_silence=100  # Keep 100ms of silence
            )
            
            current_time = 0
            for i, segment in enumerate(silent_parts):
                if i > 0:
                    # Calculate silence duration between segments
                    silence_start = current_time
                    silence_end = current_time + len(segment)
                    
                    silence_segments.append({
                        'start': silence_start / 1000.0,
                        'end': silence_end / 1000.0,
                        'duration': len(segment) / 1000.0
                    })
                
                current_time += len(segment)
            
            return silence_segments
            
        except Exception as e:
            print(f"Error in gap analysis: {e}")
            return []
    
    def adjust_speech_timing(self, audio_path: str, target_duration: float, 
                           preserve_pitch: bool = True) -> str:
        """
        Adjust speech timing to match target duration while preserving quality
        """
        try:
            # Load audio with librosa for better time-stretching
            y, sr = librosa.load(audio_path)
            
            # Calculate current duration and stretch ratio
            current_duration = len(y) / sr
            stretch_ratio = target_duration / current_duration
            
            # Time-stretch the audio
            if preserve_pitch:
                # Use phase vocoder for pitch preservation
                y_stretched = librosa.effects.time_stretch(y, rate=1/stretch_ratio)
            else:
                # Simple resampling (changes pitch)
                y_stretched = librosa.resample(y, orig_sr=sr, target_sr=sr*stretch_ratio)
            
            # Save stretched audio
            stretched_path = tempfile.mktemp(suffix='.wav')
            sf.write(stretched_path, y_stretched, sr)
            
            return stretched_path
            
        except Exception as e:
            print(f"Error in timing adjustment: {e}")
            return audio_path
