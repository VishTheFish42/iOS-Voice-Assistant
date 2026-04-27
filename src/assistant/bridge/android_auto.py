from __future__ import annotations

import json
import logging
from dataclasses import dataclass

try:
    import httpx
except Exception:  # pragma: no cover - optional
    httpx = None

logger = logging.getLogger(__name__)


@dataclass
class AndroidAction:
    type: str
    payload: dict


class AndroidBridge:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def send_action(self, action: AndroidAction) -> None:
        if httpx is None:
            logger.info("Android action: %s", json.dumps(action.payload))
            return
        try:
            httpx.post(f"{self.base_url}/action", json=action.payload, timeout=0.25)
        except Exception as exc:
            logger.warning("Android bridge failed: %s", exc)
