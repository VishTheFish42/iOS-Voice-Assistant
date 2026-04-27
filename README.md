# Automotive Voice Assistant (Python)

A Python-based LLM voice assistant designed for an Android Auto-style integration. It supports navigation, music, and calling skills, with a chatty, low-latency UX that prioritizes wake word and push-to-talk flows. The architecture is cloud-first with offline fallback.

**Core goals**
- Very low perceived latency (streaming-ready pipeline stubs included)
- Cloud + offline fallbacks (ASR, LLM, TTS)
- Android Auto-style integration via an action bridge

## Architecture
- Audio input: microphone stream with VAD and wake word engine
- ASR: cloud (when connected) with offline fallback
- LLM: OpenAI (cloud) with Ollama (local) fallback
- TTS: cloud with offline fallback
- Skills: Navigation, Music, Calling
- Android bridge: sends actions to Android Auto companion app

## Quick start (PTT simulation)
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python -m assistant`

This CLI simulates push-to-talk by text input and prints responses. The audio stack is wired but uses placeholders for ASR/TTS until you integrate engines.

## Configuration
Set environment variables as needed:
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (default `gpt-4o-mini`)
- `CLOUD_ENABLED` (`1` or `0`)
- `LOCAL_LLM_MODEL` (default `llama3` for Ollama)
- `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- `VOSK_MODEL_PATH` (default `models/vosk-en-us`)
- `PIPER_MODEL_PATH` (default `models/piper-en`)
- `ANDROID_BRIDGE_HOST` and `ANDROID_BRIDGE_PORT`

## Android Auto-style integration
Android Auto requires an Android app for Media, Navigation, and Telecom integrations. This repository provides a Python assistant that emits actions to a companion Android app via HTTP.

Example outbound action payloads sent to the Android bridge:
- Navigation: `{ "type": "navigation", "query": "navigate to 123 Market Street" }`
- Music: `{ "type": "music", "command": "play lo-fi on Spotify" }`
- Calling: `{ "type": "calling", "command": "call Alex" }`

Your Android app should:
- Map `navigation` actions to the Navigation SDK or Maps intent.
- Map `music` actions to `MediaSession` and the active media app.
- Map `calling` actions to the Telecom API or dialer intent.

## Low-latency guidance
- Use streaming ASR and TTS.
- Keep wake word local and always-on.
- Cache navigation context and recent contacts.
- Use short responses (already enforced by the system prompt).

## Project structure
- `src/assistant/main.py` entrypoint
- `src/assistant/orchestrator.py` routing and system prompt
- `src/assistant/skills/` navigation, music, calling
- `src/assistant/llm/` OpenAI + Ollama clients
- `src/assistant/asr/` cloud/offline stubs
- `src/assistant/tts/` cloud/offline stubs
- `src/assistant/bridge/android_auto.py` Android action bridge

## Next integration steps
- Replace ASR stubs with streaming engines (OpenAI, Google, Vosk, Whisper.cpp).
- Replace TTS stubs with streaming engines (OpenAI, Azure, Piper).
- Implement a real wake word engine (Porcupine or OEM).
- Build the Android companion app and map actions to Android Auto APIs.

## Safety notes
- Always confirm before calling a contact and before starting navigation in unfamiliar areas.
- Minimize dialog turns while driving.

## License
MIT
