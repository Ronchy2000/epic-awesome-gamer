# -*- coding: utf-8 -*-
"""
Thin router for LLM protocol patches.

The detailed protocol implementations live under `extensions.llm_protocols`.
Business code should keep importing `apply_llm_patch` from here so the rest of
the repository does not need to know which protocol family is active.
"""

from extensions.llm_protocols import apply_llm_patch

__all__ = ["apply_llm_patch"]
