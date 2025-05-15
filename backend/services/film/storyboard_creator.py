import os
from typing import Dict, Any, List, Optional
from core.config import settings

class StoryboardCreatorService:
    """
    Service responsible for creating storyboards based on screenplays.
    Generates key scene visualizations for the short film.
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        
    async def create(
        self,
        screenplay: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a storyboard based on a screenplay.
        
        Args:
            screenplay: Dictionary containing screenplay information
            output_path: Path to save the storyboard image
            
        Returns:
            Dictionary containing storyboard information
        """
        try:
            # Create output directory if needed
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Extract screenplay text
            screenplay_text = screenplay.get("text", "")
            
            # In production, would use OpenAI DALL-E or similar to generate scene images
            # For now, create a placeholder storyboard
            
            # Log the storyboard creation process
            print(f"Creating storyboard for screenplay")
            print(f"Output path: {output_path}")
            
            # Create placeholder storyboard file
            if output_path:
                with open(output_path, "w") as f:
                    f.write(f"Placeholder for storyboard image based on screenplay")
            
            # Extract key scenes from screenplay
            key_scenes = self._extract_key_scenes(screenplay_text)
            
            return {
                "scenes": key_scenes,
                "screenplay_id": screenplay.get("id", "unknown"),
                "file_path": output_path
            }
                
        except Exception as e:
            print(f"Error creating storyboard: {str(e)}")
            # Create basic storyboard in case of error
            return self._create_basic_storyboard(screenplay, output_path)
    
    def _extract_key_scenes(self, screenplay_text: str) -> List[Dict[str, Any]]:
        """
        Extracts key scenes from screenplay text.
        In production, would use NLP to identify important scenes.
        """
        # Simple implementation - extract scenes based on "EXT." or "INT." markers
        scenes = []
        lines = screenplay_text.split("\n")
        
        current_scene = None
        scene_description = []
        
        for line in lines:
            if "EXT." in line or "INT." in line:
                # If we were already processing a scene, save it
                if current_scene:
                    scenes.append({
                        "title": current_scene,
                        "description": "\n".join(scene_description)
                    })
                
                # Start new scene
                current_scene = line.strip()
                scene_description = []
            elif current_scene and line.strip():
                scene_description.append(line.strip())
        
        # Add the last scene if there is one
        if current_scene:
            scenes.append({
                "title": current_scene,
                "description": "\n".join(scene_description)
            })
        
        # Limit to 5 key scenes for storyboard
        return scenes[:5]
    
    def _create_basic_storyboard(
        self,
        screenplay: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a basic storyboard when normal creation fails.
        """
        # Create placeholder storyboard file
        if output_path:
            with open(output_path, "w") as f:
                f.write("Placeholder for basic storyboard (error recovery)")
        
        # Create basic scenes
        basic_scenes = [
            {"title": "ACT 1: INTRODUCTION", "description": "Character introduction scene"},
            {"title": "ACT 2: CONFLICT", "description": "Main conflict scene"},
            {"title": "ACT 3: RESOLUTION", "description": "Resolution scene"}
        ]
        
        return {
            "scenes": basic_scenes,
            "screenplay_id": screenplay.get("id", "unknown"),
            "file_path": output_path
        }
