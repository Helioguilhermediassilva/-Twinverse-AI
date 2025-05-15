from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv

# Importações dos módulos internos
from api import router as api_router
from core.config import settings

# Carregar variáveis de ambiente
load_dotenv()

# Criar aplicação FastAPI
app = FastAPI(
    title="Twinverse-AI API",
    description="API para transformar frases criativas em músicas originais",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, limitar para origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router.router, prefix="/api")

# Rota raiz
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Twinverse-AI", "status": "online"}

# Verificação de saúde
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Iniciar servidor com uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
