from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    llm_base_url: str = "http://localhost:11434"
    llm_model_name: str = "llama3"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    llm_top_p: float = 0.9
    llm_timeout_seconds: int = 30
    llm_max_retries: int = 3
    llm_retry_min_wait: float = 1.0
    llm_retry_max_wait: float = 10.0
    reflection_max_iterations: int = 3
    reflection_confidence_threshold: float = 0.7

    @property
    def chat_endpoint(self) -> str:
        return f"{self.llm_base_url}/api/chat"

    @property
    def generate_endpoint(self) -> str:
        return f"{self.llm_base_url}/api/generate"


llm_config = LLMConfig()