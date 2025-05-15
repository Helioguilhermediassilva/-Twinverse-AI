import os
from typing import Dict, Any, List, Optional
from core.config import settings

class AssetCompilerService:
    """
    Service responsible for compiling assets from all previous phases
    (music, avatar, film) for use in the publication page.
    """
    
    def __init__(self):
        pass
        
    async def compile(
        self,
        music_id: str,
        avatar_id: str,
        film_id: str,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compiles assets from all previous phases.
        
        Args:
            music_id: ID of the music
            avatar_id: ID of the avatar
            film_id: ID of the film
            output_dir: Directory to save compiled assets
            
        Returns:
            Dictionary containing compiled asset information
        """
        try:
            # Create output directory if provided
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Log the compilation process
            print(f"Compiling assets from music, avatar, and film")
            print(f"Output directory: {output_dir}")
            
            # Get asset paths
            music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
            avatar_video_path = f"./storage/avatar/{avatar_id}/avatar_video.mp4"
            avatar_model_path = f"./storage/avatar/{avatar_id}/avatar_model.glb"
            film_path = f"./storage/film/{film_id}/curta_twinverse.mp4"
            screenplay_path = f"./storage/film/{film_id}/roteiro_curta.txt"
            
            # Get creative phrase from music (if available)
            phrase = "Creative Expression"
            try:
                # In production, would retrieve from database
                # For now, try to extract from a file if it exists
                lyrics_path = f"./storage/music/{music_id}/lyrics.txt"
                if os.path.exists(lyrics_path):
                    with open(lyrics_path, "r") as f:
                        lyrics = f.read()
                        # Extract first line as phrase
                        phrase = lyrics.split("\n")[0]
            except:
                pass
            
            # Copy assets to output directory if provided
            if output_dir:
                # In production, would copy files
                # For now, just create placeholder references
                with open(f"{output_dir}/assets.json", "w") as f:
                    f.write(f"""{{
                        "music_id": "{music_id}",
                        "avatar_id": "{avatar_id}",
                        "film_id": "{film_id}",
                        "music_path": "{music_path}",
                        "avatar_video_path": "{avatar_video_path}",
                        "avatar_model_path": "{avatar_model_path}",
                        "film_path": "{film_path}",
                        "screenplay_path": "{screenplay_path}",
                        "phrase": "{phrase}"
                    }}""")
            
            # Create asset URLs (in production, would be actual URLs)
            music_url = f"/api/music/{music_id}/stream"
            avatar_url = f"/api/avatar/{avatar_id}/video"
            avatar_model_url = f"/api/avatar/{avatar_id}/model"
            film_url = f"/api/film/{film_id}/video"
            screenplay_url = f"/api/film/{film_id}/screenplay"
            
            return {
                "music_id": music_id,
                "avatar_id": avatar_id,
                "film_id": film_id,
                "phrase": phrase,
                "music_url": music_url,
                "avatar_url": avatar_url,
                "avatar_model_url": avatar_model_url,
                "film_url": film_url,
                "screenplay_url": screenplay_url,
                "output_dir": output_dir
            }
                
        except Exception as e:
            print(f"Error compiling assets: {str(e)}")
            # Return basic assets in case of error
            return self._create_basic_assets(music_id, avatar_id, film_id, output_dir)
    
    def _create_basic_assets(
        self,
        music_id: str,
        avatar_id: str,
        film_id: str,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates basic asset references when normal compilation fails.
        """
        # Create basic asset URLs
        music_url = f"/api/music/{music_id}/stream"
        avatar_url = f"/api/avatar/{avatar_id}/video"
        avatar_model_url = f"/api/avatar/{avatar_id}/model"
        film_url = f"/api/film/{film_id}/video"
        screenplay_url = f"/api/film/{film_id}/screenplay"
        
        # Create placeholder file if output directory provided
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            with open(f"{output_dir}/basic_assets.json", "w") as f:
                f.write(f"""{{
                    "music_id": "{music_id}",
                    "avatar_id": "{avatar_id}",
                    "film_id": "{film_id}",
                    "phrase": "Creative Expression"
                }}""")
        
        return {
            "music_id": music_id,
            "avatar_id": avatar_id,
            "film_id": film_id,
            "phrase": "Creative Expression",
            "music_url": music_url,
            "avatar_url": avatar_url,
            "avatar_model_url": avatar_model_url,
            "film_url": film_url,
            "screenplay_url": screenplay_url,
            "output_dir": output_dir
        }
