import json
from typing import Any


class OpenAIResearchClient:
    def __init__(
        self,
        api_key: str | None,
        model: str,
        client: Any | None = None,
    ) -> None:
        self.model = model
        self._client = client or self._build_client(api_key)

    @staticmethod
    def _build_client(api_key: str | None) -> Any | None:
        if not api_key:
            return None

        try:
            from openai import OpenAI
        except ImportError:
            return None

        return OpenAI(api_key=api_key)

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def synthesize_json(self, prompt: str) -> dict[str, Any] | None:
        if self._client is None:
            return None

        response = self._client.responses.create(
            model=self.model,
            input=prompt,
        )
        output_text = getattr(response, "output_text", None)
        if not output_text:
            return None

        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError:
            return None

        if isinstance(parsed, dict):
            return parsed
        return None
