from __future__ import annotations

from dataclasses import dataclass

GOOGLE_GENAI_PROTOCOL = "google_genai"
OPENAI_COMPATIBLE_PROTOCOL = "openai_compatible"


@dataclass(frozen=True)
class LLMPresetSpec:
    name: str
    protocol: str
    display_name: str
    description: str
    default_base_url: str = ""
    default_model: str = ""
    request_api: str = "chat_completions"
    data_url_images: bool = True
    api_key_optional: bool = False
    api_key_placeholder: str = ""
    base_url_required: bool = True
    model_required: bool = True
    supports_reasoning_effort: bool = False
    supports_thinking_toggle: bool = False
    thinking_mode_strategy: str = "none"
    docs_url: str = ""


@dataclass(frozen=True)
class ResolvedLLMConfig:
    protocol: str
    preset: str
    display_name: str
    description: str
    request_api: str
    api_key: str
    base_url: str
    model: str
    data_url_images: bool
    api_key_optional: bool
    supports_reasoning_effort: bool
    supports_thinking_toggle: bool
    thinking_mode_strategy: str
    docs_url: str

    def to_log_dict(self) -> dict[str, str | bool]:
        return {
            "protocol": self.protocol,
            "preset": self.preset,
            "display_name": self.display_name,
            "base_url": self.base_url,
            "model": self.model,
            "request_api": self.request_api,
            "data_url_images": self.data_url_images,
            "supports_reasoning_effort": self.supports_reasoning_effort,
            "supports_thinking_toggle": self.supports_thinking_toggle,
            "docs_url": self.docs_url,
        }


PRESET_SPECS: dict[str, LLMPresetSpec] = {
    "gemini": LLMPresetSpec(
        name="gemini",
        protocol=GOOGLE_GENAI_PROTOCOL,
        display_name="Gemini",
        description="Gemini official API or another Google GenAI-compatible relay.",
        default_base_url="",
        default_model="gemini-2.5-pro",
        request_api="google_genai",
        data_url_images=False,
        base_url_required=False,
        docs_url="https://ai.google.dev/gemini-api/docs/vision",
    ),
    "aihubmix": LLMPresetSpec(
        name="aihubmix",
        protocol=GOOGLE_GENAI_PROTOCOL,
        display_name="AiHubMix",
        description="Gemini-compatible relay using the Google GenAI SDK surface.",
        default_base_url="https://aihubmix.com",
        default_model="gemini-2.5-pro",
        request_api="google_genai",
        data_url_images=False,
        docs_url="https://ai.google.dev/gemini-api/docs/vision",
    ),
    "openai": LLMPresetSpec(
        name="openai",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="OpenAI",
        description="Official OpenAI API. Vision-capable model required.",
        default_base_url="https://api.openai.com/v1",
        default_model="gpt-4.1-mini",
        request_api="chat_completions",
        data_url_images=True,
        docs_url="https://developers.openai.com/api/docs/guides/migrate-to-responses",
    ),
    "deepseek": LLMPresetSpec(
        name="deepseek",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="DeepSeek",
        description="DeepSeek V4 through its OpenAI-compatible API.",
        default_base_url="https://api.deepseek.com",
        default_model="deepseek-v4-pro",
        request_api="chat_completions",
        data_url_images=True,
        supports_reasoning_effort=True,
        supports_thinking_toggle=True,
        thinking_mode_strategy="deepseek_toggle",
        docs_url="https://api-docs.deepseek.com/",
    ),
    "glm": LLMPresetSpec(
        name="glm",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="GLM",
        description="GLM multimodal models through Zhipu's OpenAI-compatible API.",
        default_base_url="https://open.bigmodel.cn/api/paas/v4",
        default_model="glm-4.6v",
        request_api="chat_completions",
        data_url_images=False,
        supports_thinking_toggle=True,
        thinking_mode_strategy="glm_auto",
        docs_url="https://open.bigmodel.cn/",
    ),
    "ollama": LLMPresetSpec(
        name="ollama",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="Ollama",
        description="Local Ollama server through its OpenAI-compatible /v1 API.",
        default_base_url="http://127.0.0.1:11434/v1",
        default_model="qwen3-vl:8b",
        request_api="chat_completions",
        data_url_images=True,
        api_key_optional=True,
        api_key_placeholder="ollama",
        supports_reasoning_effort=True,
        docs_url="https://docs.ollama.com/openai",
    ),
    "minimax": LLMPresetSpec(
        name="minimax",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="MiniMax",
        description="MiniMax through its OpenAI-compatible API. Use a vision-capable model.",
        default_base_url="https://api.minimaxi.com/v1",
        default_model="MiniMax-M2.7",
        request_api="chat_completions",
        data_url_images=True,
        docs_url="https://platform.minimaxi.com/document/Intelligent%20Assistant/OpenAI%20API%20Compatibility",
    ),
    "xiaomi_mimo": LLMPresetSpec(
        name="xiaomi_mimo",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="Xiaomi MiMo",
        description="MiMo through an OpenAI-compatible endpoint. Fill the official base URL and vision-capable model from your console.",
        default_base_url="",
        default_model="",
        request_api="chat_completions",
        data_url_images=True,
        docs_url="https://mimo.mi.com/",
    ),
    "custom_openai_compatible": LLMPresetSpec(
        name="custom_openai_compatible",
        protocol=OPENAI_COMPATIBLE_PROTOCOL,
        display_name="Custom OpenAI-Compatible",
        description="Self-hosted or third-party OpenAI-compatible service.",
        default_base_url="",
        default_model="",
        request_api="chat_completions",
        data_url_images=True,
        api_key_optional=True,
    ),
}


PRESET_ALIASES = {
    "gemini": "gemini",
    "gemini_official": "gemini",
    "gemini_compatible": "gemini",
    "aihubmix": "aihubmix",
    "openai": "openai",
    "gpt": "openai",
    "deepseek": "deepseek",
    "glm": "glm",
    "ollama": "ollama",
    "minimax": "minimax",
    "mimo": "xiaomi_mimo",
    "xiaomi": "xiaomi_mimo",
    "xiaomi_mimo": "xiaomi_mimo",
    "openai_compatible": "custom_openai_compatible",
    "custom_openai_compatible": "custom_openai_compatible",
    "custom": "custom_openai_compatible",
}


def normalize_preset_name(name: str | None) -> str:
    value = str(name or "").strip().lower()
    return PRESET_ALIASES.get(value, value)


def get_preset_spec(name: str | None) -> LLMPresetSpec | None:
    normalized = normalize_preset_name(name)
    return PRESET_SPECS.get(normalized)


def supported_preset_names() -> list[str]:
    return sorted(PRESET_SPECS.keys())
