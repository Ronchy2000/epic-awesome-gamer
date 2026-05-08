# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

from hcaptcha_challenger.agent import AgentConfig
from pydantic import Field, PrivateAttr, SecretStr, model_validator
from pydantic_settings import SettingsConfigDict

from extensions.llm_protocols import apply_llm_patch
from extensions.llm_protocols.presets import (
    GOOGLE_GENAI_PROTOCOL,
    OPENAI_COMPATIBLE_PROTOCOL,
    ResolvedLLMConfig,
    get_preset_spec,
    normalize_preset_name,
    supported_preset_names,
)

# --- 核心路径定义 ---
PROJECT_ROOT = Path(__file__).parent
VOLUMES_DIR = PROJECT_ROOT.joinpath("volumes")
LOG_DIR = VOLUMES_DIR.joinpath("logs")
USER_DATA_DIR = VOLUMES_DIR.joinpath("user_data")
RUNTIME_DIR = VOLUMES_DIR.joinpath("runtime")
SCREENSHOTS_DIR = VOLUMES_DIR.joinpath("screenshots")
RECORD_DIR = VOLUMES_DIR.joinpath("record")
HCAPTCHA_DIR = VOLUMES_DIR.joinpath("hcaptcha")


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value or default


def _clean_str(value: object, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, SecretStr):
        value = value.get_secret_value()
    value = str(value).strip()
    return value or default


def _coerce_secret_input(value: object) -> str:
    return _clean_str(value, "")


def _mask_email(value: str) -> str:
    if "@" not in value:
        return value[:3] + "***" if len(value) > 3 else "***"
    local, domain = value.split("@", 1)
    if len(local) <= 2:
        local_masked = local[:1] + "***"
    else:
        local_masked = local[:2] + "***"
    return f"{local_masked}@{domain}"


def _coerce_bool(value: object, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


class EpicSettings(AgentConfig):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    # Canonical protocol-first configuration
    LLM_PROTOCOL: str = Field(
        default="",
        description="Canonical protocol family. Supported values: google_genai, openai_compatible",
    )
    LLM_PRESET: str = Field(
        default="",
        description="Canonical preset name. Examples: gemini, openai, deepseek, glm, ollama",
    )
    LLM_API_KEY: SecretStr | None = Field(default=None, description="Canonical LLM API key")
    LLM_BASE_URL: str = Field(default="", description="Canonical LLM base URL override")
    LLM_MODEL: str = Field(default="", description="Canonical default LLM model")
    LLM_THINKING_ENABLED: bool = Field(
        default=False, description="Canonical thinking toggle for presets that support it"
    )
    LLM_REASONING_EFFORT: str = Field(
        default="", description="Canonical reasoning effort for presets that support it"
    )

    # Legacy/provider-specific environment variables kept for backward compatibility
    GEMINI_API_KEY: SecretStr | None = Field(default=None, description="Gemini/AiHubMix API key")
    GEMINI_BASE_URL: str = Field(
        default="", description="Optional Gemini-compatible base URL override"
    )
    GEMINI_MODEL: str = Field(default="gemini-2.5-pro", description="Gemini default model")

    LLM_PROVIDER: str = Field(
        default="",
        description=(
            "Legacy provider alias for LLM_PRESET. "
            f"Supported values: {', '.join(supported_preset_names())}"
        ),
    )

    GLM_API_KEY: SecretStr | None = Field(default=None, description="GLM API key")
    GLM_BASE_URL: str = Field(
        default="https://open.bigmodel.cn/api/paas/v4", description="GLM OpenAI-compatible base URL"
    )
    GLM_MODEL: str = Field(default="glm-4.6v", description="GLM vision-capable default model")

    OPENAI_API_KEY: SecretStr | None = Field(default=None, description="OpenAI API key")
    OPENAI_BASE_URL: str = Field(
        default="https://api.openai.com/v1", description="OpenAI API base URL"
    )
    OPENAI_MODEL: str = Field(default="gpt-4.1-mini", description="OpenAI vision-capable model")

    DEEPSEEK_API_KEY: SecretStr | None = Field(default=None, description="DeepSeek API key")
    DEEPSEEK_BASE_URL: str = Field(
        default="https://api.deepseek.com", description="DeepSeek OpenAI-compatible base URL"
    )
    DEEPSEEK_MODEL: str = Field(default="deepseek-v4-pro", description="DeepSeek default model")
    DEEPSEEK_THINKING_ENABLED: bool = Field(
        default=False, description="Enable DeepSeek thinking mode"
    )
    DEEPSEEK_REASONING_EFFORT: str = Field(default="high", description="DeepSeek reasoning effort")

    BROWSER_BACKEND: str = Field(
        default="auto", description="Supported values: auto, camoufox, playwright"
    )

    EPIC_EMAIL: str = Field(default_factory=lambda: _env("EPIC_EMAIL"))
    EPIC_PASSWORD: SecretStr = Field(default_factory=lambda: _env("EPIC_PASSWORD"))
    DISABLE_BEZIER_TRAJECTORY: bool = Field(default=True)
    WAIT_FOR_CHALLENGE_VIEW_TO_RENDER_MS: int = Field(default=3000)

    CHALLENGE_CLASSIFIER_MODEL: str = Field(default="")
    IMAGE_CLASSIFIER_MODEL: str = Field(default="")
    SPATIAL_POINT_REASONER_MODEL: str = Field(default="")
    SPATIAL_PATH_REASONER_MODEL: str = Field(default="")

    cache_dir: Path = HCAPTCHA_DIR.joinpath(".cache")
    challenge_dir: Path = HCAPTCHA_DIR.joinpath(".challenge")
    captcha_response_dir: Path = HCAPTCHA_DIR.joinpath(".captcha")

    ENABLE_APSCHEDULER: bool = Field(default=True)
    TASK_TIMEOUT_SECONDS: int = Field(default=900)
    REDIS_URL: str = Field(default="redis://redis:6379/0")
    CELERY_WORKER_CONCURRENCY: int = Field(default=1)
    CELERY_TASK_TIME_LIMIT: int = Field(default=1200)
    CELERY_TASK_SOFT_TIME_LIMIT: int = Field(default=900)

    _resolved_llm: ResolvedLLMConfig | None = PrivateAttr(default=None)
    _requested_protocol: str = PrivateAttr(default="")

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_provider_aliases(cls, raw_data):
        data = dict(raw_data) if isinstance(raw_data, dict) else {}

        preset_candidate = _clean_str(data.get("LLM_PRESET")) or _clean_str(
            data.get("LLM_PROVIDER")
        )
        preset = normalize_preset_name(preset_candidate)
        protocol = _clean_str(data.get("LLM_PROTOCOL")).lower()

        if not preset:
            if _coerce_secret_input(data.get("DEEPSEEK_API_KEY")) or _clean_str(
                data.get("DEEPSEEK_MODEL")
            ):
                preset = "deepseek"
            elif _coerce_secret_input(data.get("OPENAI_API_KEY")) or _clean_str(
                data.get("OPENAI_MODEL")
            ):
                preset = "openai"
            elif _coerce_secret_input(data.get("GLM_API_KEY")) or _clean_str(data.get("GLM_MODEL")):
                preset = "glm"
            elif _coerce_secret_input(data.get("GEMINI_API_KEY")) or _clean_str(
                data.get("GEMINI_MODEL")
            ):
                preset = "gemini"
            elif protocol == OPENAI_COMPATIBLE_PROTOCOL:
                preset = "custom_openai_compatible"
            elif protocol == GOOGLE_GENAI_PROTOCOL:
                preset = "gemini"

        if preset:
            data["LLM_PRESET"] = preset
            data["LLM_PROVIDER"] = preset

        if not data.get("LLM_PROTOCOL"):
            spec = get_preset_spec(preset)
            if spec:
                data["LLM_PROTOCOL"] = spec.protocol

        llm_api_key = _coerce_secret_input(data.get("LLM_API_KEY"))
        if not llm_api_key:
            legacy_key_map = {
                "openai": _coerce_secret_input(data.get("OPENAI_API_KEY")),
                "deepseek": _coerce_secret_input(data.get("DEEPSEEK_API_KEY")),
                "glm": _coerce_secret_input(data.get("GLM_API_KEY")),
                "gemini": _coerce_secret_input(data.get("GEMINI_API_KEY")),
                "aihubmix": _coerce_secret_input(data.get("GEMINI_API_KEY")),
                "ollama": "",
                "minimax": "",
                "xiaomi_mimo": "",
                "custom_openai_compatible": "",
            }
            legacy_key = legacy_key_map.get(preset, "")
            if legacy_key:
                data["LLM_API_KEY"] = legacy_key

        if not _clean_str(data.get("LLM_BASE_URL")):
            legacy_base_url_map = {
                "openai": _clean_str(data.get("OPENAI_BASE_URL")),
                "deepseek": _clean_str(data.get("DEEPSEEK_BASE_URL")),
                "glm": _clean_str(data.get("GLM_BASE_URL")),
                "gemini": _clean_str(data.get("GEMINI_BASE_URL")),
                "aihubmix": _clean_str(data.get("GEMINI_BASE_URL")),
            }
            legacy_base_url = legacy_base_url_map.get(preset, "")
            if legacy_base_url:
                data["LLM_BASE_URL"] = legacy_base_url

        if not _clean_str(data.get("LLM_MODEL")):
            legacy_model_map = {
                "openai": _clean_str(data.get("OPENAI_MODEL")),
                "deepseek": _clean_str(data.get("DEEPSEEK_MODEL")),
                "glm": _clean_str(data.get("GLM_MODEL")),
                "gemini": _clean_str(data.get("GEMINI_MODEL")),
                "aihubmix": _clean_str(data.get("GEMINI_MODEL")),
            }
            legacy_model = legacy_model_map.get(preset, "")
            if legacy_model:
                data["LLM_MODEL"] = legacy_model

        if not _clean_str(data.get("LLM_REASONING_EFFORT")):
            deepseek_effort = _clean_str(data.get("DEEPSEEK_REASONING_EFFORT"))
            if preset == "deepseek" and deepseek_effort:
                data["LLM_REASONING_EFFORT"] = deepseek_effort

        if data.get("LLM_THINKING_ENABLED") in {None, ""}:
            if preset == "deepseek":
                data["LLM_THINKING_ENABLED"] = _coerce_bool(
                    data.get("DEEPSEEK_THINKING_ENABLED"), default=False
                )

        return data

    @model_validator(mode="after")
    def _apply_runtime_defaults(self):
        for field_name in (
            "LLM_PROTOCOL",
            "LLM_PRESET",
            "LLM_PROVIDER",
            "LLM_BASE_URL",
            "LLM_MODEL",
            "LLM_REASONING_EFFORT",
            "GEMINI_BASE_URL",
            "GEMINI_MODEL",
            "GLM_BASE_URL",
            "GLM_MODEL",
            "OPENAI_BASE_URL",
            "OPENAI_MODEL",
            "DEEPSEEK_BASE_URL",
            "DEEPSEEK_MODEL",
            "DEEPSEEK_REASONING_EFFORT",
            "BROWSER_BACKEND",
            "EPIC_EMAIL",
            "CHALLENGE_CLASSIFIER_MODEL",
            "IMAGE_CLASSIFIER_MODEL",
            "SPATIAL_POINT_REASONER_MODEL",
            "SPATIAL_PATH_REASONER_MODEL",
        ):
            value = getattr(self, field_name, None)
            if isinstance(value, str):
                setattr(self, field_name, value.strip())

        preset_name = normalize_preset_name(self.LLM_PRESET or self.LLM_PROVIDER)
        spec = get_preset_spec(preset_name)
        if spec is None:
            fallback = (
                "deepseek"
                if self.DEEPSEEK_API_KEY
                else "openai" if self.OPENAI_API_KEY else "glm" if self.GLM_API_KEY else "gemini"
            )
            preset_name = normalize_preset_name(fallback)
            spec = get_preset_spec(preset_name)
        assert spec is not None

        self.LLM_PRESET = preset_name
        self.LLM_PROVIDER = preset_name
        requested_protocol = _clean_str(self.LLM_PROTOCOL, "").lower()
        self._requested_protocol = requested_protocol
        self.LLM_PROTOCOL = spec.protocol

        api_key = _coerce_secret_input(self.LLM_API_KEY)
        if not api_key:
            legacy_key_map = {
                "openai": _coerce_secret_input(self.OPENAI_API_KEY),
                "deepseek": _coerce_secret_input(self.DEEPSEEK_API_KEY),
                "glm": _coerce_secret_input(self.GLM_API_KEY),
                "gemini": _coerce_secret_input(self.GEMINI_API_KEY),
                "aihubmix": _coerce_secret_input(self.GEMINI_API_KEY),
            }
            api_key = legacy_key_map.get(preset_name, "")
        if not api_key and spec.api_key_optional and spec.api_key_placeholder:
            api_key = spec.api_key_placeholder

        base_url = _clean_str(self.LLM_BASE_URL, "")
        if not base_url:
            legacy_base_url_map = {
                "openai": self.OPENAI_BASE_URL,
                "deepseek": self.DEEPSEEK_BASE_URL,
                "glm": self.GLM_BASE_URL,
                "gemini": self.GEMINI_BASE_URL,
                "aihubmix": self.GEMINI_BASE_URL,
            }
            base_url = _clean_str(legacy_base_url_map.get(preset_name), "")
        if not base_url:
            base_url = spec.default_base_url

        model = _clean_str(self.LLM_MODEL, "")
        if not model:
            legacy_model_map = {
                "openai": self.OPENAI_MODEL,
                "deepseek": self.DEEPSEEK_MODEL,
                "glm": self.GLM_MODEL,
                "gemini": self.GEMINI_MODEL,
                "aihubmix": self.GEMINI_MODEL,
            }
            model = _clean_str(legacy_model_map.get(preset_name), "")
        if not model:
            model = spec.default_model

        thinking_enabled = self.LLM_THINKING_ENABLED
        if preset_name == "deepseek" and not self.LLM_THINKING_ENABLED:
            thinking_enabled = self.DEEPSEEK_THINKING_ENABLED
        self.LLM_THINKING_ENABLED = bool(thinking_enabled)

        reasoning_effort = _clean_str(self.LLM_REASONING_EFFORT, "")
        if preset_name == "deepseek" and not reasoning_effort:
            reasoning_effort = _clean_str(self.DEEPSEEK_REASONING_EFFORT, "")
        self.LLM_REASONING_EFFORT = reasoning_effort

        if self.GEMINI_API_KEY is None:
            # `hcaptcha-challenger` still carries Gemini-shaped assumptions in its config model.
            # Seed a compatible token so the adapter layer can take over for non-Google protocols.
            bridge_key = api_key or (spec.api_key_placeholder if spec.api_key_optional else "")
            if bridge_key:
                self.GEMINI_API_KEY = SecretStr(bridge_key)

        self._resolved_llm = ResolvedLLMConfig(
            protocol=self.LLM_PROTOCOL,
            preset=preset_name,
            display_name=spec.display_name,
            description=spec.description,
            request_api=spec.request_api,
            api_key=api_key,
            base_url=base_url,
            model=model,
            data_url_images=spec.data_url_images,
            api_key_optional=spec.api_key_optional,
            supports_reasoning_effort=spec.supports_reasoning_effort,
            supports_thinking_toggle=spec.supports_thinking_toggle,
            thinking_mode_strategy=spec.thinking_mode_strategy,
            docs_url=spec.docs_url,
        )

        provider_default = model
        if not self.CHALLENGE_CLASSIFIER_MODEL:
            self.CHALLENGE_CLASSIFIER_MODEL = provider_default
        if not self.IMAGE_CLASSIFIER_MODEL:
            self.IMAGE_CLASSIFIER_MODEL = provider_default
        if not self.SPATIAL_POINT_REASONER_MODEL:
            self.SPATIAL_POINT_REASONER_MODEL = provider_default
        if not self.SPATIAL_PATH_REASONER_MODEL:
            self.SPATIAL_PATH_REASONER_MODEL = provider_default

        browser_backend = (self.BROWSER_BACKEND or "").strip().lower()
        self.BROWSER_BACKEND = browser_backend or "auto"

        return self

    @property
    def resolved_llm(self) -> ResolvedLLMConfig:
        assert self._resolved_llm is not None
        return self._resolved_llm

    @property
    def masked_epic_email(self) -> str:
        return _mask_email(self.EPIC_EMAIL)

    @property
    def user_data_dir(self) -> Path:
        target_ = self.user_data_dir_for("camoufox")
        return target_

    def user_data_dir_for(self, backend: str) -> Path:
        backend = (backend or "camoufox").strip().lower()
        suffix = f".{backend}"
        target_ = USER_DATA_DIR.joinpath(f"{self.EPIC_EMAIL}{suffix}")
        target_.mkdir(parents=True, exist_ok=True)
        return target_

    @property
    def llm_configuration_error(self) -> str | None:
        resolved = self.resolved_llm

        if self._requested_protocol and self._requested_protocol != resolved.protocol:
            return (
                "Invalid LLM configuration: "
                f"LLM_PROTOCOL={self._requested_protocol} conflicts with preset {resolved.preset} "
                f"which belongs to protocol {resolved.protocol}."
            )

        if not resolved.api_key and not resolved.api_key_optional:
            return (
                "Invalid LLM configuration: "
                f"preset={resolved.preset} requires an API key. "
                "Fill LLM_API_KEY or the matching legacy provider key."
            )

        spec = get_preset_spec(resolved.preset)
        if spec and spec.base_url_required and not resolved.base_url:
            return (
                "Invalid LLM configuration: "
                f"preset={resolved.preset} requires a base URL. "
                "Fill LLM_BASE_URL or the matching legacy base URL field."
            )

        if spec and spec.model_required and not resolved.model:
            return (
                "Invalid LLM configuration: "
                f"preset={resolved.preset} requires a model name. "
                "Fill LLM_MODEL or the matching legacy provider model field."
            )

        return None


settings = EpicSettings()
settings.ignore_request_questions = ["Please drag the crossing to complete the lines"]
apply_llm_patch(settings)
