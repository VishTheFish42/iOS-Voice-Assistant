from __future__ import annotations

from .base import SkillResult
from .calling import CallingSkill
from .music import MusicSkill
from .navigation import NavigationSkill


class SkillRouter:
    def __init__(self):
        self.skills = [NavigationSkill(), MusicSkill(), CallingSkill()]

    def route(self, text: str) -> SkillResult | None:
        for skill in self.skills:
            if skill.can_handle(text):
                return skill.handle(text)
        return None
