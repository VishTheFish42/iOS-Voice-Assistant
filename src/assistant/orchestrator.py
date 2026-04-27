from __future__ import annotations

import logging
from dataclasses import dataclass

from .bridge.android_auto import AndroidAction, AndroidBridge
from .config import AssistantConfig
from .llm.router import LLMRouter
from .skills.router import SkillRouter
from .tts.base import TTSEngine

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = (
    "You are an in-car voice assistant. Be concise, confident, and friendly. "
    "If the request is about navigation, music, or calling, confirm the action. "
    "If you need clarification, ask a short follow-up. "
    "Keep responses under two short sentences."
)


@dataclass
class AssistantResponse:
    text: str
    action: dict | None = None


class AssistantOrchestrator:
    def __init__(self, config: AssistantConfig, llm: LLMRouter, tts: TTSEngine, bridge: AndroidBridge):
        self.config = config
        self.llm = llm
        self.tts = tts
        self.bridge = bridge
        self.skills = SkillRouter()

    def handle_text(self, text: str) -> AssistantResponse:
        if not text.strip():
            return AssistantResponse(text="")

        skill_result = self.skills.route(text)
        if skill_result is not None:
            if skill_result.action:
                self.bridge.send_action(AndroidAction(type=skill_result.action["type"], payload=skill_result.action))
            return AssistantResponse(text=skill_result.text, action=skill_result.action)

        response = self.llm.generate(prompt=text, system=SYSTEM_PROMPT)
        return AssistantResponse(text=response.text or "Okay.")

    def speak(self, text: str) -> None:
        # Placeholder for streaming TTS playback. TTS integration is needed here.
        _ = self.tts.synthesize(text)
