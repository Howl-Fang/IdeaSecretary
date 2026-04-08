import json
from typing import Any

from openai import OpenAI

from app.config import settings
from app.prompts import SYSTEM_PROMPT_CHAT, SYSTEM_PROMPT_ORGANIZE


class AIClient:
    def __init__(self) -> None:
        self.enabled = bool(settings.openai_api_key)
        if self.enabled:
            kwargs: dict[str, Any] = {"api_key": settings.openai_api_key}
            if settings.openai_base_url:
                kwargs["base_url"] = settings.openai_base_url
            self.client = OpenAI(**kwargs)
        else:
            self.client = None

    def _safe_parse_json(self, content: str) -> dict[str, Any]:
        try:
            parsed = json.loads(content)
            if not isinstance(parsed, dict):
                raise ValueError("AI response is not object")
            return parsed
        except Exception:
            return {
                "summary": content,
                "tags": ["unstructured"],
                "follow_up_questions": ["Can you provide more detail?"],
                "insight": "Unable to parse model output into JSON, returned raw content.",
            }

    def organize_note(self, raw_content: str) -> dict[str, Any]:
        if not self.enabled:
            short = raw_content[:140]
            return {
                "summary": short,
                "tags": ["draft"],
                "follow_up_questions": ["What action should we take next?"],
                "insight": "AI key not configured; using deterministic local summary.",
            }

        completion = self.client.responses.create(
            model=settings.openai_model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT_ORGANIZE},
                {"role": "user", "content": raw_content},
            ],
        )
        content = completion.output_text or "{}"
        parsed = self._safe_parse_json(content)
        if "summary" not in parsed:
            parsed["summary"] = raw_content[:140]
        if "insight" not in parsed:
            parsed["insight"] = "No additional insight generated."
        return parsed

    def chat(self, question: str, context: str) -> str:
        if not self.enabled:
            return f"[Local mode] Based on your notes: {context[:220]}"

        completion = self.client.responses.create(
            model=settings.openai_model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT_CHAT},
                {"role": "user", "content": f"Question: {question}\n\nKnowledge Base:\n{context}"},
            ],
        )
        return completion.output_text or "I could not generate a response."


ai_client = AIClient()
