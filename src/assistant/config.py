import os
from dataclasses import dataclass


def _env(key: str, default: str | None = None) -> str | None:
    value = os.environ.get(key)
    return value if value is not None else default


@dataclass(frozen=True)
class AssistantConfig:
    # Core
    name: str = _env("ASSISTANT_NAME", "Ava") or "Ava"
    locale: str = _env("ASSISTANT_LOCALE", "en-US") or "en-US"
    log_level: str = _env("ASSISTANT_LOG_LEVEL", "INFO") or "INFO"

    # Wake word + PTT
    wake_word_enabled: bool = (_env("WAKE_WORD_ENABLED", "1") == "1")
    ptt_enabled: bool = (_env("PTT_ENABLED", "1") == "1")

    # Cloud connectivity
    cloud_enabled: bool = (_env("CLOUD_ENABLED", "1") == "1")
    openai_api_key: str | None = _env("OPENAI_API_KEY")
    openai_model: str = _env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"

    # Local model
    local_llm_provider: str = _env("LOCAL_LLM_PROVIDER", "ollama") or "ollama"
    local_llm_model: str = _env("LOCAL_LLM_MODEL", "llama3") or "llama3"
    ollama_base_url: str = _env("OLLAMA_BASE_URL", "http://localhost:11434") or "http://localhost:11434"

    # ASR
    cloud_asr_provider: str = _env("CLOUD_ASR_PROVIDER", "openai") or "openai"
    offline_asr_provider: str = _env("OFFLINE_ASR_PROVIDER", "vosk") or "vosk"
    vosk_model_path: str = _env("VOSK_MODEL_PATH", "models/vosk-en-us") or "models/vosk-en-us"

    # TTS
    cloud_tts_provider: str = _env("CLOUD_TTS_PROVIDER", "openai") or "openai"
    offline_tts_provider: str = _env("OFFLINE_TTS_PROVIDER", "piper") or "piper"
    piper_model_path: str = _env("PIPER_MODEL_PATH", "models/piper-en") or "models/piper-en"

    # Audio
    sample_rate: int = int(_env("AUDIO_SAMPLE_RATE", "16000") or "16000")
    chunk_ms: int = int(_env("AUDIO_CHUNK_MS", "20") or "20")

    # Android bridge
    android_bridge_host: str = _env("ANDROID_BRIDGE_HOST", "0.0.0.0") or "0.0.0.0"
    android_bridge_port: int = int(_env("ANDROID_BRIDGE_PORT", "8088") or "8088")

    # Latency budget (ms)
    target_latency_ms: int = int(_env("TARGET_LATENCY_MS", "250") or "250")
