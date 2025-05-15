import requests
from typing import Optional
from fastapi import UploadFile
import os
from core.config import settings

class VoiceProcessorService:
    """
    Serviço responsável por processar a voz do usuário ou gerar voz sintética.
    Utiliza a API do ElevenLabs ou Respeecher para síntese de voz.
    """
    
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        
    async def process(
        self,
        lyrics: str,
        emotion: str,
        voice_file: Optional[UploadFile] = None,
        output_path: str = None
    ) -> str:
        """
        Processa a voz do usuário ou gera voz sintética para a letra da música.
        
        Args:
            lyrics: Letra da música
            emotion: Emoção dominante
            voice_file: Arquivo de voz do usuário (opcional)
            output_path: Caminho para salvar o arquivo de áudio
            
        Returns:
            Caminho do arquivo de voz processado
        """
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Se o usuário forneceu um arquivo de voz
            if voice_file:
                # Em uma implementação real, processaríamos o arquivo de voz
                # e aplicaríamos à letra da música
                print(f"Processando arquivo de voz do usuário: {voice_file.filename}")
                
                # Simular processamento de voz do usuário
                with open(output_path, "w") as f:
                    f.write(f"Simulação de arquivo MP3 - Voz do usuário processada")
                    
            else:
                # Caso contrário, gerar voz sintética
                print(f"Gerando voz sintética para emoção: {emotion}")
                print(f"Letra: {lyrics[:100]}...")
                
                # Em uma implementação real, chamaríamos a API do ElevenLabs
                # Aqui, simulamos o processo para exemplo
                
                # Simular geração de voz sintética
                with open(output_path, "w") as f:
                    f.write(f"Simulação de arquivo MP3 - Voz sintética para {emotion}")
            
            return output_path
            
        except Exception as e:
            # Em caso de erro, registrar e retornar caminho para um arquivo padrão
            print(f"Erro ao processar voz: {str(e)}")
            
            # Criar arquivo de fallback
            with open(output_path, "w") as f:
                f.write("Arquivo de voz de fallback")
                
            return output_path
