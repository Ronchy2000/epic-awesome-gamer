from __future__ import annotations

from typing import Any

from extensions.llm_protocols.google_genai import apply_google_genai_patch
from extensions.llm_protocols.openai_compatible import apply_openai_compatible_patch
from extensions.llm_protocols.presets import GOOGLE_GENAI_PROTOCOL, OPENAI_COMPATIBLE_PROTOCOL


def apply_llm_patch(settings: Any):
    protocol = settings.resolved_llm.protocol
    if protocol == OPENAI_COMPATIBLE_PROTOCOL:
        apply_openai_compatible_patch(settings)
        return
    if protocol == GOOGLE_GENAI_PROTOCOL:
        apply_google_genai_patch(settings)
        return
    raise ValueError(f"Unsupported LLM protocol: {protocol}")
