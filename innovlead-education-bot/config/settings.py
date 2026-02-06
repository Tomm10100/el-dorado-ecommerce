"""
Settings and configuration management using Pydantic
Loads configuration from environment variables
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Telegram Configuration
    telegram_bot_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    bot_mode: str = Field(default='polling', env='BOT_MODE')
    webhook_url: Optional[str] = Field(default=None, env='WEBHOOK_URL')
    webhook_port: int = Field(default=8443, env='WEBHOOK_PORT')
    
    # AI Provider Configuration
    ai_provider: str = Field(default='anthropic', env='AI_PROVIDER')
    anthropic_api_key: Optional[str] = Field(default=None, env='ANTHROPIC_API_KEY')
    anthropic_model: str = Field(default='claude-3-sonnet-20240229', env='ANTHROPIC_MODEL')
    openai_api_key: Optional[str] = Field(default=None, env='OPENAI_API_KEY')
    openai_model: str = Field(default='gpt-4-turbo-preview', env='OPENAI_MODEL')
    
    # Database Configuration
    database_url: str = Field(default='sqlite:///innovlead_bot.db', env='DATABASE_URL')
    
    # Security
    secret_key: str = Field(default='change-me-in-production', env='SECRET_KEY')
    environment: str = Field(default='development', env='ENVIRONMENT')
    
    # Logging
    log_level: str = Field(default='INFO', env='LOG_LEVEL')
    log_file: str = Field(default='logs/bot.log', env='LOG_FILE')
    
    # PIPEDA Compliance
    data_retention_days: int = Field(default=365, env='DATA_RETENTION_DAYS')
    anonymize_after_inactive_days: int = Field(default=730, env='ANONYMIZE_AFTER_INACTIVE_DAYS')
    require_data_consent: bool = Field(default=True, env='REQUIRE_DATA_CONSENT')
    
    # n8n Integration (Optional)
    n8n_webhook_url: Optional[str] = Field(default=None, env='N8N_WEBHOOK_URL')
    n8n_api_key: Optional[str] = Field(default=None, env='N8N_API_KEY')
    
    # CRA Reporting
    cra_reporting_enabled: bool = Field(default=True, env='CRA_REPORTING_ENABLED')
    cra_report_frequency: str = Field(default='monthly', env='CRA_REPORT_FREQUENCY')
    cra_report_email: str = Field(default='reports@innovlead.org', env='CRA_REPORT_EMAIL')
    
    # Rate Limiting
    rate_limit_messages_per_hour: int = Field(default=30, env='RATE_LIMIT_MESSAGES_PER_HOUR')
    rate_limit_ai_queries_per_day: int = Field(default=20, env='RATE_LIMIT_AI_QUERIES_PER_DAY')
    
    # Localization
    default_language: str = Field(default='en', env='DEFAULT_LANGUAGE')
    supported_languages: str = Field(default='en,es,fr', env='SUPPORTED_LANGUAGES')
    
    # Feature Flags
    enable_ai_tutor: bool = Field(default=True, env='ENABLE_AI_TUTOR')
    enable_quizzes: bool = Field(default=True, env='ENABLE_QUIZZES')
    enable_certificates: bool = Field(default=True, env='ENABLE_CERTIFICATES')
    enable_community: bool = Field(default=False, env='ENABLE_COMMUNITY')
    
    # Organization Details
    org_name: str = Field(default='InnovLead Foundation', env='ORG_NAME')
    org_website: str = Field(default='https://innovlead.org', env='ORG_WEBSITE')
    org_email: str = Field(default='education@innovlead.org', env='ORG_EMAIL')
    org_telegram_community: str = Field(default='@InnovLeadCommunity', env='ORG_TELEGRAM_COMMUNITY')
    executive_director: str = Field(default='Tommy Fernandez', env='EXECUTIVE_DIRECTOR')
    technical_chair: str = Field(default='William Melendez', env='TECHNICAL_CHAIR')
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = 'ignore'  # Ignore extra fields from parent .env


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create settings instance (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
