import httpx
from typing import Dict, Optional
from .models import AskResponse


class Client:
    def __init__(self, base_url: str):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url

    def ask(self, question: str, context: Optional[Dict] = None) -> AskResponse:
        url = f"{self.base_url}/ask"
        payload = {
            "question": question,
            "context": context or {}
        }

        try:
            response = httpx.post(url, json=payload, timeout=30)
        except httpx.RequestError as e:
            raise RuntimeError(f"Could not reach backend: {e}") from e

        if response.status_code != 200:
            raise RuntimeError(
                f"Server error {response.status_code}: {response.text}"
            )

        # response.json is a dict containing JSON string from backend
        result_dict = response.json()
        # Ensure formatting and types
        return AskResponse(
            answer=result_dict.get("answer", ""),
            confidence=result_dict.get("confidence", 0.0),
            risk=result_dict.get("risk", "unknown"),
            reasons=result_dict.get("reasons", []),
            sources=result_dict.get("sources", [])
        )
