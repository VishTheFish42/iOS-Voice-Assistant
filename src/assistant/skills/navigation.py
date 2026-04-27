from __future__ import annotations

from .base import Skill, SkillResult


class NavigationSkill(Skill):
    name = "navigation"

    def can_handle(self, text: str) -> bool:
        triggers = ["navigate", "directions", "route", "drive to", "take me to", "map"]
        lowered = text.lower()
        return any(t in lowered for t in triggers)

    def handle(self, text: str) -> SkillResult:
        return SkillResult(
            text="Got it. Starting navigation.",
            action={"type": "navigation", "query": text},
        )
