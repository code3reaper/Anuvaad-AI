import { useState } from 'react';
import './App.css';
import VideoDubbing from './components/VideoDubbing';
import YoutubeSummarizer from './components/YoutubeSummarizer';
import WordToStory from './components/WordToStory';
import ArticleToPodcast from './components/ArticleToPodcast';
import TextToSpeech from './components/TextToSpeech';
import SpeechToText from './components/SpeechToText';
import TextTranslation from './components/TextTranslation';

function App() {
  const [activeFeature, setActiveFeature] = useState(null);

  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">🌐 Anuvaad AI</h1>
      </header>

      <div className="hero">
        <h1>Professional Video Dubbing & Content Transformation</h1>
        <p className="subtitle">
          Transform your content across languages with AI-powered dubbing, translation, and creative tools
        </p>
      </div>

      <div className="main-content">
        <h2 style={{ textAlign: 'center', margin: '1rem 0 2rem 0' }}>Main Features</h2>
        
        <div className="features-grid">
          <div className="feature-card">
            <h3>🎬 Video Dubbing</h3>
            <VideoDubbing />
          </div>

          <div className="feature-card">
            <h3>📺 YouTube Summarizer</h3>
            <YoutubeSummarizer />
          </div>

          <div className="feature-card">
            <h3>📖 Word to Story</h3>
            <WordToStory />
          </div>

          <div className="feature-card">
            <h3>🎙️ Article to Podcast</h3>
            <ArticleToPodcast />
          </div>
        </div>

        <hr className="divider" />

        <h2 style={{ textAlign: 'center', margin: '2rem 0' }}>Additional Tools</h2>

        <div className="tool-buttons">
          <button 
            className={`tool-btn ${activeFeature === 'tts' ? 'active' : ''}`}
            onClick={() => setActiveFeature(activeFeature === 'tts' ? null : 'tts')}
          >
            🗣️ Text to Speech
          </button>
          <button 
            className={`tool-btn ${activeFeature === 'stt' ? 'active' : ''}`}
            onClick={() => setActiveFeature(activeFeature === 'stt' ? null : 'stt')}
          >
            🎤 Speech to Text
          </button>
          <button 
            className={`tool-btn ${activeFeature === 'trans' ? 'active' : ''}`}
            onClick={() => setActiveFeature(activeFeature === 'trans' ? null : 'trans')}
          >
            🌐 Text Translation
          </button>
        </div>

        {activeFeature === 'tts' && <TextToSpeech />}
        {activeFeature === 'stt' && <SpeechToText />}
        {activeFeature === 'trans' && <TextTranslation />}
      </div>
    </div>
  );
}

export default App;
