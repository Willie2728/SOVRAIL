import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    db_path: str = os.getenv('SOVRAIL_DB_PATH', 'sovrail.db')
    master_key: str | None = os.getenv('SOVRAIL_MASTER_KEY')
    ollama_url: str = os.getenv('OLLAMA_URL', 'http://host.docker.internal:11434')
    local_model: str = os.getenv('SOVRAIL_LOCAL_MODEL', 'llama3.2')
    openai_key: str | None = os.getenv('OPENAI_API_KEY')
    openai_model: str | None = os.getenv('OPENAI_DEFAULT_MODEL')
    anthropic_key: str | None = os.getenv('ANTHROPIC_API_KEY')
    anthropic_model: str | None = os.getenv('ANTHROPIC_DEFAULT_MODEL')
    tavus_key: str | None = os.getenv('TAVUS_API_KEY')
    require_signatures: bool = os.getenv('SOVRAIL_REQUIRE_SIGNATURES', 'false').lower() == 'true'
    signature_skew_seconds: int = int(os.getenv('SOVRAIL_SIGNATURE_SKEW_SECONDS', '300'))
    request_timeout: int = int(os.getenv('SOVRAIL_REQUEST_TIMEOUT', '180'))
    cache_namespace: str = os.getenv('SOVRAIL_CACHE_NAMESPACE', 'default')
    allowed_tavus_host: str = os.getenv('SOVRAIL_TAVUS_HOST', 'https://tavusapi.com')

settings = Settings()
