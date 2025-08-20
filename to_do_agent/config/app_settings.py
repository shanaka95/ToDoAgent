"""
Application Settings - Configuring Your ToDo Agent

This module contains the main configuration settings for your ToDo Agent application.
Think of it as the "control panel" that determines how your application behaves,
where it runs, and how it connects to external services.

The settings include:
- Basic application info (name, version, environment)
- Server configuration (which port to run on)
- API keys for AI services (OpenAI, Anthropic)
- Model preferences and connection settings

These settings can be changed through environment variables, making it easy
to configure the app for different environments (development, production, etc.).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppSettings(BaseSettings):
    """
    Main application configuration settings.
    
    This class holds all the settings that control how your ToDo Agent
    application works. It uses environment variables for configuration,
    so you can easily change settings without modifying code.
    
    All environment variables should start with "app_" to avoid conflicts
    with other parts of the system.
    """

    model_config = SettingsConfigDict(env_prefix="app_")

    # Basic Application Information
    environment: str = Field(
        default="development", 
        description="Current environment (development, production, testing, etc.)"
    )
    service_name: str = Field(
        default="to-do-agent", 
        description="The name of your application (used in logs and API docs)"
    )
    version: str = Field(
        default="0.1.0", 
        description="Current version of your application"
    )

    # Server Configuration
    port: int = Field(
        default=8086, 
        description="Which port the web server should run on"
    )