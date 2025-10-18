<<<<<<< HEAD
<!--
README for Anuvaad-AI
This file is modeled after the Plant Care Pro sample the user provided.
-->

# 🎬 Anuvaad-AI — AI-Powered Multilingual Dubbing & Media Studio

<div align="center">

![Anuvaad-AI Logo](https://img.shields.io/badge/Anuvaad--AI-AI_Powered-brightgreen?style=for-the-badge&logo=ai)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-orange.svg?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18%2B-cyan.svg?style=for-the-badge&logo=react)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-7+-violet.svg?style=for-the-badge&logo=vite)](https://vitejs.dev)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-purple.svg?style=for-the-badge)](https://elevenlabs.io)
[![Gemini](https://img.shields.io/badge/Gemini-Google_AI-blueviolet.svg?style=for-the-badge)](https://ai.google/)

</div>

Anuvaad-AI helps creators and teams convert media into multilingual content: dubbing, transcription, TTS, translation, and creative audio/video utilities — all powered by modern AI services.

---

## ✨ Highlights

- 🎥 Video dubbing with synchronized audio and language mapping
- 🗣️ Speech-to-text transcription and subtitle generation
- 🔊 Text-to-speech (ElevenLabs + fallback options)
- 🌐 AI translation & content generation (Google Gemini)
- 📰 Article → Podcast, Word → Story, YouTube summarizer
- ⚙️ Media processing with FFmpeg, MoviePy, and Pydub

---

## 🚀 Quick Start (Windows PowerShell)

1. Clone repository

```powershell
git clone https://github.com/code3reaper/Anuvaad-AI.git
cd Anuvaad-AI
```

2. Create & activate Python venv

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install Python deps

```powershell
pip install --upgrade pip
pip install -r app_requirements.txt
```

4. Install frontend deps (Node.js 18+, npm)

```powershell
cd frontend
npm install
cd ..
```

5. Create `.env` from `.env.example` and fill keys

```powershell
copy .env.example .env
notepad .env
```

Required env keys (examples):
- ELEVENLABS_API_KEY=your_elevenlabs_key
- GEMINI_API_KEY=your_gemini_key
- JWT_SECRET_KEY=your_jwt_secret

6. Start both servers

```powershell
python start.py
```

Open UI: http://localhost:5000

---

## 📁 Project layout (important files)

```
Anuvaad-AI/
├── start.py                # launcher: starts backend + frontend
├── backend.py              # Flask backend (API)
├── app_requirements.txt    # Python dependencies
├── frontend/               # React + Vite app
├── elevenlabs_dubbing.py   # ElevenLabs TTS helper
├── video_processor.py      # FFmpeg/MoviePy helpers
├── article_to_podcast.py   # article -> podcast workflow
├── story_generator.py      # word -> story generator
├── attached_assets/        # misc scripts (no secrets checked in)
└── README.md               # this file
```

---

## 🔌 High-level API endpoints

- `GET /api/health` — health check
- `POST /api/text-to-speech` — generate audio from text
- `POST /api/speech-to-text` — transcribe audio
- `POST /api/translate` — translate text
- `POST /api/youtube/summary` — summarize YouTube video
- `POST /api/video-dubbing/start` — begin dubbing job
- `GET /api/video-dubbing/status/<id>` — job status
- `GET /api/video-dubbing/download/<id>` — download output

Check `frontend/src` for concrete examples of request payloads.

---

## 🛠 Development notes

- Run backend only:

```powershell
.
\venv\Scripts\Activate
python backend.py
```

- Run frontend only:

```powershell
cd frontend
npm run dev -- --host 0.0.0.0 --port 5000
```

- `start.py` will:
   - ensure `.env` exists
   - check Node/npm availability
   - run `npm install` in `frontend` if required
   - start backend and frontend and stream logs

---

## 🔧 Troubleshooting

- `.env file not found`: copy `.env.example` and fill keys
- `npm not found`: install Node.js and reopen terminal
- `FFmpeg not found`: install FFmpeg and add to PATH
- `ImportError` for ElevenLabs/Gemini: ensure correct package versions and API keys
- If you accidentally committed secrets: rotate keys and scrub history (I can help)

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit your changes
4. Push and open a Pull Request

Please keep secrets out of commits — use `.env` and `.env.example`.

---

## 📝 License

MIT — see `LICENSE`.

---

If you'd like, I can also:

- add a polished `.env.example` and ensure `.gitignore` excludes `.env`
- create a small GitHub Actions workflow (lint/tests)
- add badges and sample screenshots to this README

Enjoy — tell me if you want the README adjusted (more badges, images or a demo GIF).

## ✨ Features


## 🚀 Quick Start

### Prerequisites


### Installation

1. **Clone the repository**
   ```bash
   cd anuvaad-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r app_requirements.txt
   ```

5. **Configure API keys**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys:
   - Get ElevenLabs key: https://elevenlabs.io/app/settings/api-keys
   - Get Gemini key: https://ai.google.dev/

### Run the App

Just one command:

```bash
python start.py
```

That's it! 🎉

The app will be available at **http://localhost:5000**

Press `Ctrl+C` to stop.

## 📁 Project Structure

```
anuvaad-ai/
├── start.py              # 🚀 Single command to start everything
├── .env.example          # Template for API keys
├── .env                  # Your API keys (create this)
├── app_requirements.txt  # Python dependencies
├── backend.py            # Flask backend
├── frontend/             # React frontend
└── ...
```

## 🔑 API Keys

You need:

1. **ElevenLabs** (AI voice generation)
   - Sign up: https://elevenlabs.io/
   - Get key: https://elevenlabs.io/app/settings/api-keys

2. **Google Gemini** (AI translation)
   - Get key: https://ai.google.dev/

## 📖 Documentation

See `setup_guide.txt` for detailed setup instructions and troubleshooting.

## 🛠️ Tech Stack


## 💡 Usage Tips


## 🐛 Common Issues

**Module not found?**
```bash
pip install -r app_requirements.txt
```

**FFmpeg not found?**
Install FFmpeg and add to PATH

**Port in use?**
Stop other apps using ports 5000/5001

## 📝 License

All rights reserved.


Made with ❤️ by Anuvaad AI Team
=======
# Anuvaad-AI
AI-powered multilingual video dubbing, TTS, transcription and translation application
>>>>>>> origin/main
