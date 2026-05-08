from __future__ import annotations

from typing import Any

from loguru import logger

from extensions.llm_protocols.common import ensure_list, guess_mime_type, load_binary


def apply_google_genai_patch(settings: Any):
    resolved = settings.resolved_llm
    if not resolved.api_key:
        return

    try:
        from google import genai
        from google.genai import types

        orig_init = genai.Client.__init__

        def new_init(self, *args, **kwargs):
            kwargs["api_key"] = resolved.api_key

            base_url = resolved.base_url.rstrip("/")
            if base_url:
                if base_url.endswith("/v1"):
                    base_url = base_url[:-3]
                if not base_url.endswith("/gemini"):
                    base_url = f"{base_url}/gemini"
                kwargs["http_options"] = types.HttpOptions(base_url=base_url)
                logger.info(
                    "LLM patch applied | protocol={} | preset={} | model={} | base_url={}",
                    resolved.protocol,
                    resolved.preset,
                    resolved.model,
                    base_url,
                )
            else:
                logger.info(
                    "LLM patch applied | protocol={} | preset={} | model={} | base_url=google-default",
                    resolved.protocol,
                    resolved.preset,
                    resolved.model,
                )

            orig_init(self, *args, **kwargs)

        genai.Client.__init__ = new_init

        file_cache: dict[str, bytes] = {}

        async def patched_upload(self_files, file, **kwargs):
            content = load_binary(file)
            file_id = f"bypass_{id(content)}"
            file_cache[file_id] = content
            return types.File(name=file_id, uri=file_id, mime_type=guess_mime_type(file))

        orig_generate = genai.models.AsyncModels.generate_content

        async def patched_generate(self_models, model, contents, **kwargs):
            normalized = ensure_list(contents)
            for content in normalized:
                for index, part in enumerate(ensure_list(getattr(content, "parts", None))):
                    file_data = getattr(part, "file_data", None)
                    file_uri = getattr(file_data, "file_uri", None) if file_data else None
                    if file_uri in file_cache:
                        content.parts[index] = types.Part.from_bytes(
                            data=file_cache[file_uri], mime_type=guess_mime_type(file_uri)
                        )

            return await orig_generate(self_models, model=model, contents=normalized, **kwargs)

        genai.files.AsyncFiles.upload = patched_upload
        genai.models.AsyncModels.generate_content = patched_generate
        logger.info("Gemini file upload compatibility patch enabled")
    except Exception as exc:
        logger.error("Google GenAI compatibility patch failed: {}", exc)
