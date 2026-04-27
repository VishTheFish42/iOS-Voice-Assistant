from __future__ import annotations

from .base import Skill, SkillResult


class CallingSkill(Skill):
    name = "calling"

    def can_handle(self, text: str) -> bool:
        triggers = ["call", "dial", "ring", "hang up", "end call"]
        lowered = text.lower()
        return any(t in lowered for t in triggers)

    def handle(self, text: str) -> SkillResult:
        return SkillResult(
            text="Calling now.",
            action={"type": "calling", "command": text},
        )
