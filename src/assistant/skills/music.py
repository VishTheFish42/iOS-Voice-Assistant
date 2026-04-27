from __future__ import annotations

from .base import Skill, SkillResult


class MusicSkill(Skill):
    name = "music"

    def can_handle(self, text: str) -> bool:
        triggers = ["play", "pause", "resume", "next song", "previous", "skip", "shuffle", "volume"]
        lowered = text.lower()
        return any(t in lowered for t in triggers)

    def handle(self, text: str) -> SkillResult:
        return SkillResult(
            text="Sure. Updating your music.",
            action={"type": "music", "command": text},
        )
