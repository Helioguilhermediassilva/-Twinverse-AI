from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from typing import Optional
import os
from pydantic import BaseModel

# Importações dos serviços
from services.phrase_interpreter import PhraseInterpreterService
from services.lyrics_generator import LyricsGeneratorService
from services.music_generator import MusicGeneratorService
from services.voice_processor import VoiceProcessorService

router = APIRouter(tags=["music"])

# Modelos de dados
class MusicRequest(BaseModel):
    phrase: str
    genre: Optional[str] = None
    emotion: Optional[str] = None
    
class MusicResponse(BaseModel):
    id: str
    phrase: str
    lyrics: str
    music_url: str
    status: str

# Endpoints
@router.post("/music/create", response_model=MusicResponse)
async def create_music(
    phrase: str = Form(...),
    genre: Optional[str] = Form(None),
    emotion: Optional[str] = Form(None),
    voice_file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Cria uma música original a partir de uma frase criativa.
    
    - **phrase**: Frase criativa que inspirará a música
    - **genre**: (Opcional) Gênero musical desejado
    - **emotion**: (Opcional) Emoção principal desejada
    - **voice_file**: (Opcional) Arquivo de voz do usuário
    """
    try:
        # Gerar ID único para a música
        music_id = f"music_{phrase[:10].replace(' ', '_').lower()}_{os.urandom(4).hex()}"
        
        # Processar a frase para extrair emoção, palavras-chave e gênero sugerido
        phrase_interpreter = PhraseInterpreterService()
        interpretation = await phrase_interpreter.interpret(phrase, emotion, genre)
        
        # Gerar letra da música
        lyrics_generator = LyricsGeneratorService()
        lyrics = await lyrics_generator.generate(
            phrase=phrase,
            emotion=interpretation["emotion"],
            genre=interpretation["genre"],
            keywords=interpretation["keywords"]
        )
        
        # Iniciar processo de geração de música em background
        # (Este processo pode demorar, então é executado em background)
        background_tasks.add_task(
            process_music_generation,
            music_id=music_id,
            phrase=phrase,
            lyrics=lyrics,
            emotion=interpretation["emotion"],
            genre=interpretation["genre"],
            voice_file=voice_file
        )
        
        return {
            "id": music_id,
            "phrase": phrase,
            "lyrics": lyrics,
            "music_url": f"/api/music/{music_id}/stream",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar música: {str(e)}")

@router.get("/music/{music_id}")
async def get_music_status(music_id: str):
    """
    Verifica o status de geração de uma música.
    """
    # Verificar se a música existe e seu status
    # Implementação simplificada - em produção, verificaria em banco de dados
    music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
    
    if os.path.exists(music_path):
        return {
            "id": music_id,
            "status": "completed",
            "music_url": f"/api/music/{music_id}/stream"
        }
    else:
        return {
            "id": music_id,
            "status": "processing"
        }

@router.get("/music/{music_id}/stream")
async def stream_music(music_id: str):
    """
    Retorna o arquivo de música para streaming.
    """
    music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
    
    if not os.path.exists(music_path):
        raise HTTPException(status_code=404, detail="Música não encontrada ou ainda em processamento")
    
    return FileResponse(
        path=music_path,
        media_type="audio/mpeg",
        filename=f"twinverse_{music_id}.mp3"
    )

# Função auxiliar para processamento em background
async def process_music_generation(
    music_id: str,
    phrase: str,
    lyrics: str,
    emotion: str,
    genre: str,
    voice_file: Optional[UploadFile] = None
):
    try:
        # Criar diretório para armazenar arquivos da música
        os.makedirs(f"./storage/music/{music_id}", exist_ok=True)
        
        # Salvar letra da música
        with open(f"./storage/music/{music_id}/lyrics.txt", "w") as f:
            f.write(lyrics)
        
        # Gerar melodia instrumental
        music_generator = MusicGeneratorService()
        instrumental_path = await music_generator.generate(
            lyrics=lyrics,
            emotion=emotion,
            genre=genre,
            output_path=f"./storage/music/{music_id}/instrumental.mp3"
        )
        
        # Processar voz (do usuário ou sintética)
        voice_processor = VoiceProcessorService()
        voice_path = await voice_processor.process(
            lyrics=lyrics,
            emotion=emotion,
            voice_file=voice_file,
            output_path=f"./storage/music/{music_id}/voice.mp3"
        )
        
        # Combinar instrumental e voz
        final_music_path = await music_generator.combine(
            instrumental_path=instrumental_path,
            voice_path=voice_path,
            output_path=f"./storage/music/{music_id}/musica_finalizada.mp3"
        )
        
        # Em uma implementação real, atualizaríamos o status no banco de dados
        
    except Exception as e:
        # Registrar erro e atualizar status
        with open(f"./storage/music/{music_id}/error.log", "w") as f:
            f.write(f"Erro ao gerar música: {str(e)}")
