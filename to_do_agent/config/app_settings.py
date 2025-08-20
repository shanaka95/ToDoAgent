from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppSettings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(env_prefix="app_")

    # Environment configuration
    environment: str = Field(default="development", description="Environment")

    # Service identification
    service_name: str = Field(default="to-do-agent", description="Name of the service")
    version: str = Field(default="0.1.0", description="Service version")

    # Runtime configuration
    port: int = 8086

    # LLM settings
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    model_name: str = Field(default="claude-3-5-sonnet-20241022", description="Model name")
    
    # OpenAI settings
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_base_url: str = Field(default="https://api.openai.com/v1", description="OpenAI base URL for custom endpoints")