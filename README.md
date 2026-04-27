# iOS Voice Assistant

A native iOS voice assistant built in Swift, powered by GPT-4o-mini. Speak a command and the app transcribes it, routes it to the right action, and responds — all hands-free. Currently designed for everyday phone use, with a roadmap toward in-car / automotive integration.

## Features

- Push-to-talk mic button with live transcription
- GPT-4o-mini for natural language responses
- Built-in skills that bypass the LLM for instant execution:
  - **Navigation** — opens Apple Maps or Google Maps with turn-by-turn directions
  - **Music** — launches Spotify, Apple Music, or any installed music app
  - **Calling** — dials a contact or number directly

## Requirements

- Xcode 15+
- iOS 17+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Clone the repo and open `ios/VoiceAssistant.xcodeproj` in Xcode
2. In `ios/VoiceAssistant/Config.swift`, replace `YOUR_API_KEY_HERE` with your OpenAI API key
3. Select your device and hit **Run**

Grant microphone and speech recognition permissions when prompted on first launch.

## Architecture

| Layer | Detail |
|---|---|
| UI | SwiftUI |
| Speech recognition | `SFSpeechRecognizer` (on-device, en-US) |
| LLM | OpenAI `gpt-4o-mini` via REST |
| TTS | `AVSpeechSynthesizer` (on-device) |
| Skills | Keyword-matched router → `AppLauncher` |

## Roadmap

- Conversation memory (multi-turn context)
- Streaming LLM responses for lower perceived latency
- Swap on-device TTS for OpenAI TTS for a more natural voice
- Background operation — runs silently and handles calls, navigation, and music without needing to open the app or say a wake word
- CarPlay / automotive integration — once background phone operation is stable, adapt the same architecture for in-car use

## License

MIT
