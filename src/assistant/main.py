from __future__ import annotations

import logging

from .bridge.android_auto import AndroidBridge
from .config import AssistantConfig
from .llm.ollama_client import OllamaClient
from .llm.openai_client import OpenAIClient
from .llm.router import LLMRouter
from .orchestrator import AssistantOrchestrator
from .tts.cloud import CloudTTS
from .tts.offline import OfflineTTS


def build_orchestrator(config: AssistantConfig) -> AssistantOrchestrator:
    cloud_llm = OpenAIClient(api_key=config.openai_api_key, model=config.openai_model)
    local_llm = OllamaClient(base_url=config.ollama_base_url, model=config.local_llm_model)
    llm_router = LLMRouter(cloud=cloud_llm, local=local_llm, cloud_enabled=config.cloud_enabled)

    cloud_tts = CloudTTS(provider=config.cloud_tts_provider)
    offline_tts = OfflineTTS(provider=config.offline_tts_provider, model_path=config.piper_model_path)
    tts = cloud_tts if config.cloud_enabled else offline_tts

    bridge = AndroidBridge(base_url=f"http://{config.android_bridge_host}:{config.android_bridge_port}")
    return AssistantOrchestrator(config=config, llm=llm_router, tts=tts, bridge=bridge)


def main() -> None:
    config = AssistantConfig()
    logging.basicConfig(level=config.log_level)
    assistant = build_orchestrator(config)

    print(f"{config.name} ready. Type commands (simulate PTT). Ctrl+C to exit.")
    while True:
        try:
            text = input("> ").strip()
        except EOFError:
            break
        response = assistant.handle_text(text)
        if response.text:
            print(f"{config.name}: {response.text}")
            assistant.speak(response.text)


if __name__ == "__main__":
    main()
