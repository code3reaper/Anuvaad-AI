import { useState } from 'react';
import { useAuth } from './AuthContext';
import './App.css';
import Header from './components/Header';
import Hero from './components/Hero';
import SearchBar from './components/SearchBar';
import FeatureRow from './components/FeatureRow';
import Footer from './components/Footer';
import FeatureModal from './components/FeatureModal';
import LoginModal from './components/LoginModal';
import VideoDubbing from './components/VideoDubbing';
import YoutubeSummarizer from './components/YoutubeSummarizer';
import WordToStory from './components/WordToStory';
import ArticleToPodcast from './components/ArticleToPodcast';
import TextToSpeech from './components/TextToSpeech';
import SpeechToText from './components/SpeechToText';
import TextTranslation from './components/TextTranslation';

function App() {
  const [selectedFeature, setSelectedFeature] = useState(null);
  const [activeComponent, setActiveComponent] = useState(null);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);
  const { isAuthenticated } = useAuth();

  const coreFeatures = [
    {
      icon: '🎬',
      title: 'Video Dubbing',
      shortDesc: 'Professional AI-powered video dubbing across multiple languages',
      description: 'Transform your videos with professional AI-powered dubbing. Our advanced technology maintains voice quality and emotional tone while translating your content into multiple languages, making your videos accessible to global audiences.',
      details: [
        'Support for 50+ languages',
        'Natural voice synthesis',
        'Lip-sync optimization',
        'High-quality audio output',
        'Batch processing support'
      ],
      image: '/attached_assets/stock_images/video_dubbing_microp_c08e1bb8.jpg',
      component: VideoDubbing,
      id: 'video-dubbing'
    },
    {
      icon: '📺',
      title: 'YouTube Summarizer',
      shortDesc: 'Get instant AI-generated summaries of YouTube videos',
      description: 'Save time with instant AI-generated summaries of YouTube videos. Our intelligent system extracts key points, main topics, and essential information, allowing you to grasp video content in minutes instead of hours.',
      details: [
        'Accurate content extraction',
        'Key point identification',
        'Timestamp references',
        'Multi-language support',
        'Customizable summary length'
      ],
      image: '/attached_assets/stock_images/youtube_video_conten_6e650ebb.jpg',
      component: YoutubeSummarizer,
      id: 'youtube-summarizer'
    },
    {
      icon: '📖',
      title: 'Word to Story',
      shortDesc: 'Transform simple words into engaging creative stories',
      description: 'Unleash your creativity by transforming simple words or phrases into rich, engaging stories. Our AI storyteller uses advanced language models to craft compelling narratives that capture imagination and deliver meaningful content.',
      details: [
        'Creative narrative generation',
        'Multiple genre options',
        'Customizable story length',
        'Character development',
        'Plot structure optimization'
      ],
      image: '/attached_assets/stock_images/creative_storytellin_0ade6655.jpg',
      component: WordToStory,
      id: 'word-to-story'
    },
    {
      icon: '🎙️',
      title: 'Article to Podcast',
      shortDesc: 'Convert written articles into engaging audio podcasts',
      description: 'Convert your written articles and blog posts into professional audio podcasts. Perfect for content creators who want to reach audiences on-the-go with natural-sounding voice narration and engaging audio presentation.',
      details: [
        'Natural voice narration',
        'Multiple voice options',
        'Background music support',
        'Professional audio quality',
        'MP3 export format'
      ],
      image: '/attached_assets/stock_images/podcast_microphone_a_4eec9237.jpg',
      component: ArticleToPodcast,
      id: 'article-to-podcast'
    }
  ];

  const advancedTools = [
    {
      icon: '🗣️',
      title: 'Text to Speech',
      shortDesc: 'Convert text into natural-sounding speech',
      description: 'Convert any text into natural-sounding speech with our advanced text-to-speech technology. Choose from multiple voices, accents, and languages to create professional voiceovers and audio content.',
      details: [
        'Multiple voice options',
        'Natural intonation',
        'Speed control',
        'High-quality audio',
        'Batch conversion'
      ],
      image: '/attached_assets/stock_images/text_to_speech_ai_te_2a30ee21.jpg',
      component: TextToSpeech,
      id: 'text-to-speech'
    },
    {
      icon: '🎤',
      title: 'Speech to Text',
      shortDesc: 'Transcribe audio into accurate text',
      description: 'Accurately transcribe audio recordings into text with our speech recognition technology. Perfect for creating transcripts, subtitles, or converting voice notes into written format.',
      details: [
        'High accuracy transcription',
        'Real-time processing',
        'Multi-language support',
        'Timestamp generation',
        'Speaker identification'
      ],
      image: '/attached_assets/stock_images/speech_recognition_v_e7a309ac.jpg',
      component: SpeechToText,
      id: 'speech-to-text'
    },
    {
      icon: '🌐',
      title: 'Text Translation',
      shortDesc: 'Translate text between multiple languages instantly',
      description: 'Break language barriers with instant text translation. Our AI-powered translation service supports multiple languages and maintains context and meaning for accurate, natural translations.',
      details: [
        '100+ language pairs',
        'Context-aware translation',
        'Instant results',
        'Idiomatic expressions',
        'Batch translation support'
      ],
      image: '/attached_assets/stock_images/translation_language_3cf3ff8e.jpg',
      component: TextTranslation,
      id: 'text-translation'
    }
  ];

  const handleCardClick = (feature) => {
    if (!isAuthenticated) {
      setShowLoginPrompt(true);
      return;
    }
    setSelectedFeature(feature);
  };

  const handleFeatureAction = (feature) => {
    if (!isAuthenticated) {
      setShowLoginPrompt(true);
      return;
    }
    
    setActiveComponent(feature.id);
    setSelectedFeature(null);
    
    setTimeout(() => {
      const element = document.getElementById('active-feature-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  const handleSearch = (searchTerm) => {
    console.log('Searching for:', searchTerm);
  };

  const getActiveComponent = () => {
    const allFeatures = [...coreFeatures, ...advancedTools];
    const feature = allFeatures.find(f => f.id === activeComponent);
    return feature?.component || null;
  };

  const ActiveComponent = getActiveComponent();

  return (
    <div className="app-netflix">
      <Header onSearchChange={handleSearch} />
      
      <Hero />
      
      <SearchBar onSearch={handleSearch} />
      
      <section id="features" className="features-section">
        <FeatureRow 
          title="Core Features" 
          features={coreFeatures}
          onCardClick={(feature) => {
            handleCardClick({ ...feature, action: () => handleFeatureAction(feature) });
          }}
        />
        
        <FeatureRow 
          title="Advanced Tools" 
          features={advancedTools}
          onCardClick={(feature) => {
            handleCardClick({ ...feature, action: () => handleFeatureAction(feature) });
          }}
        />
      </section>

      {activeComponent && (
        <section id="active-feature-section" className="active-feature-section">
          <div className="active-feature-container">
            <button 
              className="close-feature-btn" 
              onClick={() => setActiveComponent(null)}
            >
              ← Back to Features
            </button>
            {ActiveComponent && <ActiveComponent />}
          </div>
        </section>
      )}
      
      <Footer />
      
      {selectedFeature && (
        <FeatureModal 
          feature={selectedFeature} 
          onClose={() => setSelectedFeature(null)} 
        />
      )}
      
      {showLoginPrompt && (
        <LoginModal 
          onClose={() => setShowLoginPrompt(false)}
          onSwitchToSignup={() => setShowLoginPrompt(false)}
        />
      )}
    </div>
  );
}

export default App;
