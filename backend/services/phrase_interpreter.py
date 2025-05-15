import openai
from typing import Dict, List, Optional
from core.config import settings

class PhraseInterpreterService:
    """
    Serviço responsável por interpretar a frase criativa do usuário,
    identificando emoção dominante, palavras-chave e gênero musical sugerido.
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def interpret(
        self, 
        phrase: str, 
        user_emotion: Optional[str] = None,
        user_genre: Optional[str] = None
    ) -> Dict:
        """
        Interpreta a frase criativa do usuário.
        
        Args:
            phrase: Frase criativa do usuário
            user_emotion: Emoção especificada pelo usuário (opcional)
            user_genre: Gênero musical especificado pelo usuário (opcional)
            
        Returns:
            Dicionário contendo emoção dominante, palavras-chave e gênero musical sugerido
        """
        # Se o usuário já especificou emoção e gênero, usamos esses valores
        if user_emotion and user_genre:
            return {
                "emotion": user_emotion,
                "genre": user_genre,
                "keywords": self._extract_keywords(phrase)
            }
        
        # Caso contrário, usamos a IA para interpretar a frase
        prompt = f"""
        Analise a seguinte frase criativa e identifique:
        1. A emoção dominante (uma palavra)
        2. Três palavras-chave principais
        3. Um gênero musical que melhor se adequaria a essa frase
        
        Frase: "{phrase}"
        
        Responda no formato JSON:
        {{
            "emotion": "emoção identificada",
            "keywords": ["palavra1", "palavra2", "palavra3"],
            "genre": "gênero musical sugerido"
        }}
        """
        
        # Em uma implementação real, chamaríamos a API da OpenAI
        # Aqui, simulamos uma resposta para exemplo
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em análise de texto e música."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = response.choices[0].message.content
            # Converter string JSON para dicionário Python
            import json
            interpretation = json.loads(result)
            
            # Sobrescrever com valores do usuário, se fornecidos
            if user_emotion:
                interpretation["emotion"] = user_emotion
            if user_genre:
                interpretation["genre"] = user_genre
                
            return interpretation
            
        except Exception as e:
            # Em caso de erro, retornar valores padrão
            return {
                "emotion": user_emotion or "alegria",
                "genre": user_genre or "pop",
                "keywords": self._extract_keywords(phrase)
            }
    
    def _extract_keywords(self, phrase: str) -> List[str]:
        """
        Extrai palavras-chave da frase (método simplificado).
        Em uma implementação real, usaríamos NLP mais avançado.
        """
        # Remover pontuação e converter para minúsculas
        import re
        clean_phrase = re.sub(r'[^\w\s]', '', phrase.lower())
        
        # Remover stopwords (simplificado)
        stopwords = ["o", "a", "os", "as", "um", "uma", "e", "de", "da", "do", "em", "para", "com", "por"]
        words = [word for word in clean_phrase.split() if word not in stopwords]
        
        # Retornar até 3 palavras mais longas como palavras-chave
        words.sort(key=len, reverse=True)
        return words[:3]
