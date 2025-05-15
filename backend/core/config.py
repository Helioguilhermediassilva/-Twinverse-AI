import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Informações da aplicação
    APP_NAME: str = "Twinverse-AI"
    APP_VERSION: str = "0.1.0"
    
    # Configurações do servidor
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Diretórios
    STORAGE_DIR: str = "./storage"
    MUSIC_DIR: str = "./storage/music"
    TEMP_DIR: str = "./storage/temp"
    
    # Chaves de API (em produção, usar variáveis de ambiente)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SUNO_API_KEY: str = os.getenv("SUNO_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    # Configurações de CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instância única das configurações
settings = Settings()

# Garantir que os diretórios de armazenamento existam
os.makedirs(settings.MUSIC_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)
