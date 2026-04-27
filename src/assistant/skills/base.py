from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SkillResult:
    text: str
    action: dict | None = None


class Skill:
    name: str = ""

    def can_handle(self, text: str) -> bool:
        raise NotImplementedError

    def handle(self, text: str) -> SkillResult:
        raise NotImplementedError
