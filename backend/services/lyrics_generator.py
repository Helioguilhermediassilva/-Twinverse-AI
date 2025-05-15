import openai
from typing import Dict, Optional
from core.config import settings

class LyricsGeneratorService:
    """
    Serviço responsável por gerar letras de música com base na frase criativa,
    emoção dominante, palavras-chave e gênero musical.
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate(
        self,
        phrase: str,
        emotion: str,
        genre: str,
        keywords: list
    ) -> str:
        """
        Gera letra de música com estrutura definida.
        
        Args:
            phrase: Frase criativa do usuário
            emotion: Emoção dominante
            genre: Gênero musical
            keywords: Palavras-chave extraídas da frase
            
        Returns:
            Letra completa da música
        """
        prompt = f"""
        Crie uma letra de música em português brasileiro baseada na seguinte frase criativa:
        "{phrase}"
        
        A música deve:
        - Transmitir a emoção: {emotion}
        - Ser do gênero: {genre}
        - Incorporar as palavras-chave: {', '.join(keywords)}
        - Seguir a estrutura: Verso 1, Pré-refrão, Refrão, Verso 2, Refrão final
        - Ter um refrão repetitivo, mas sem repetir palavras mais de 4 vezes
        - Ser coerente com a mensagem da frase original
        
        Formate a letra claramente indicando cada seção (VERSO 1, PRÉ-REFRÃO, REFRÃO, etc.)
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um compositor de músicas talentoso."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            lyrics = response.choices[0].message.content
            return lyrics
            
        except Exception as e:
            # Em caso de erro, retornar uma letra genérica
            return self._generate_fallback_lyrics(phrase, emotion, genre)
    
    def _generate_fallback_lyrics(self, phrase: str, emotion: str, genre: str) -> str:
        """
        Gera uma letra de música simples em caso de falha na API.
        """
        return f"""
        VERSO 1
        {phrase}
        Palavras que ecoam em minha mente
        Sentimentos de {emotion} que não consigo esconder
        No ritmo de {genre} que me faz viver
        
        PRÉ-REFRÃO
        E agora vou cantar
        O que meu coração quer falar
        
        REFRÃO
        {phrase}
        É o que me faz seguir
        {phrase}
        É o que me faz sentir
        
        VERSO 2
        Cada palavra tem um significado
        Cada nota uma emoção
        Nessa jornada que escolhi
        Encontro a minha direção
        
        REFRÃO FINAL
        {phrase}
        É o que me faz seguir
        {phrase}
        É o que me faz sentir
        """
