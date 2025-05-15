import openai
from typing import Dict, Any, Optional
import os
from core.config import settings

class ScreenplayGeneratorService:
    """
    Service responsible for generating screenplays for short films
    based on music and avatar.
    """
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
    async def generate(
        self,
        music_id: str,
        avatar_id: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a screenplay for a short film based on music and avatar.
        
        Args:
            music_id: ID of the music
            avatar_id: ID of the avatar
            output_path: Path to save the screenplay file
            
        Returns:
            Dictionary containing screenplay information
        """
        try:
            # Create output directory if needed
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # In production, would retrieve music and avatar data from database
            # For now, simulate with placeholder paths
            music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
            lyrics_path = f"./storage/music/{music_id}/lyrics.txt"
            avatar_path = f"./storage/avatar/{avatar_id}/avatar_video.mp4"
            
            # Read lyrics if available
            lyrics = "Placeholder lyrics for demonstration"
            if os.path.exists(lyrics_path):
                try:
                    with open(lyrics_path, "r") as f:
                        lyrics = f.read()
                except:
                    pass
            
            # Generate screenplay using OpenAI
            prompt = f"""
            Create a screenplay for a short film based on the following music lyrics:
            
            {lyrics}
            
            The film should have 3 acts:
            1. Introduction (who is the character)
            2. Conflict (message of the music represented visually)
            3. Resolution (transformation or catharsis)
            
            The main character is represented by an avatar with ID {avatar_id}.
            The film should be 2-5 minutes long and align with the emotional tone of the music.
            
            Format the screenplay with scene descriptions, character actions, and minimal dialogue.
            """
            
            # In production, would call OpenAI API
            # For now, generate a placeholder screenplay
            screenplay_text = self._generate_placeholder_screenplay(lyrics)
            
            # Save screenplay to file if output path provided
            if output_path:
                with open(output_path, "w") as f:
                    f.write(screenplay_text)
            
            return {
                "text": screenplay_text,
                "music_id": music_id,
                "avatar_id": avatar_id,
                "acts": 3,
                "estimated_duration": "3:30",
                "file_path": output_path
            }
                
        except Exception as e:
            print(f"Error generating screenplay: {str(e)}")
            # Generate basic screenplay in case of error
            screenplay_text = self._generate_fallback_screenplay()
            
            # Save fallback screenplay to file if output path provided
            if output_path:
                with open(output_path, "w") as f:
                    f.write(screenplay_text)
            
            return {
                "text": screenplay_text,
                "music_id": music_id,
                "avatar_id": avatar_id,
                "acts": 3,
                "estimated_duration": "2:00",
                "file_path": output_path
            }
    
    def _generate_placeholder_screenplay(self, lyrics: str) -> str:
        """
        Generates a placeholder screenplay based on lyrics.
        In production, would use OpenAI API.
        """
        # Extract a few lines from lyrics for demonstration
        lyrics_excerpt = lyrics[:100] + "..." if len(lyrics) > 100 else lyrics
        
        return f"""TWINVERSE SHORT FILM SCREENPLAY

TITLE: "TRANSFORMATION"

ACT 1: INTRODUCTION
------------------

FADE IN:

EXT. CITY STREET - DAY

We see our PROTAGONIST walking alone through a busy street. Their face shows a mix of determination and uncertainty. The world around them moves quickly, but they seem disconnected from it.

PROTAGONIST (V.O.)
{lyrics_excerpt}

The protagonist stops at a crossroads, looking in different directions, unsure which path to take.

ACT 2: CONFLICT
--------------

EXT. STORM - EVENING

Dark clouds gather. The protagonist faces increasing obstacles, metaphorically representing the emotional journey in the music.

Rain begins to fall as the protagonist struggles against the elements, each step becoming more difficult.

PROTAGONIST
(looking up at the sky)
I won't give up.

The storm intensifies, mirroring the emotional crescendo of the music.

ACT 3: RESOLUTION
----------------

EXT. HILLTOP - SUNRISE

The storm has passed. Our protagonist reaches the top of a hill as the sun rises, symbolizing transformation and new beginnings.

The world looks different now - brighter, full of possibility. The protagonist's expression has changed from uncertainty to peaceful confidence.

PROTAGONIST (V.O.)
(final lyrics from the song)

The protagonist takes a deep breath, smiles, and walks toward the sunrise.

FADE OUT.

THE END
"""
    
    def _generate_fallback_screenplay(self) -> str:
        """
        Generates a basic fallback screenplay in case of errors.
        """
        return """TWINVERSE SHORT FILM SCREENPLAY

TITLE: "JOURNEY"

ACT 1: INTRODUCTION
------------------

FADE IN:

EXT. PARK - DAY

We meet our PROTAGONIST sitting alone on a bench, contemplating life.

ACT 2: CONFLICT
--------------

EXT. FOREST PATH - DAY

The protagonist navigates through a challenging path, facing obstacles that represent their inner struggles.

ACT 3: RESOLUTION
----------------

EXT. CLEARING - SUNSET

The protagonist emerges from the forest into a beautiful clearing, finding peace and resolution.

FADE OUT.

THE END
"""
