from __future__ import annotations

from typing import Any

from loguru import logger

from extensions.llm_protocols.common import OpenAICompatibleGenAIClient


def apply_openai_compatible_patch(settings: Any):
    resolved = settings.resolved_llm
    if not resolved.api_key and not resolved.api_key_optional:
        return

    try:
        from google import genai

        genai.Client = OpenAICompatibleGenAIClient
        logger.info(
            "LLM patch applied | protocol={} | preset={} | model={} | base_url={}",
            resolved.protocol,
            resolved.preset,
            resolved.model,
            resolved.base_url,
        )
    except Exception as exc:
        logger.error("OpenAI-compatible patch failed: {}", exc)
