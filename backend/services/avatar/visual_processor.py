import requests
from typing import Optional, Dict, Any
from fastapi import UploadFile
import os
from core.config import settings

class VisualProcessorService:
    """
    Service responsible for processing visual input (description or image)
    to extract features for avatar creation.
    """
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        
    async def process(
        self,
        description: Optional[str] = None,
        image_file: Optional[UploadFile] = None,
        style: str = "realistic"
    ) -> Dict[str, Any]:
        """
        Processes visual input to extract features for avatar creation.
        
        Args:
            description: Textual description of desired avatar appearance
            image_file: User's selfie or reference image
            style: Visual style (realistic, cartoon, anime, futuristic)
            
        Returns:
            Dictionary containing visual features for avatar creation
        """
        try:
            # Create temporary directory if needed
            os.makedirs(settings.TEMP_DIR, exist_ok=True)
            
            # Process based on input type
            if image_file:
                # Process uploaded image
                return await self._process_image(image_file, style)
            elif description:
                # Process textual description
                return await self._process_description(description, style)
            else:
                # Generate default avatar if no input provided
                return self._generate_default_avatar(style)
                
        except Exception as e:
            print(f"Error processing visual input: {str(e)}")
            # Return default features in case of error
            return self._generate_default_avatar(style)
    
    async def _process_image(self, image_file: UploadFile, style: str) -> Dict[str, Any]:
        """
        Processes uploaded image to extract features.
        In production, would use computer vision APIs.
        """
        # Save uploaded file temporarily
        temp_path = f"{settings.TEMP_DIR}/{image_file.filename}"
        with open(temp_path, "wb") as f:
            content = await image_file.read()
            f.write(content)
        
        # In production, would call vision API to extract features
        # For now, return simulated features
        return {
            "source_type": "image",
            "style": style,
            "features": {
                "face_shape": "oval",
                "skin_tone": "medium",
                "hair_color": "brown",
                "hair_style": "short",
                "eye_color": "brown",
                "facial_features": {
                    "eyes": "round",
                    "nose": "medium",
                    "mouth": "medium"
                }
            },
            "source_path": temp_path
        }
    
    async def _process_description(self, description: str, style: str) -> Dict[str, Any]:
        """
        Processes textual description to extract features.
        In production, would use NLP and text-to-image APIs.
        """
        # In production, would call OpenAI API to interpret description
        # For now, return simulated features based on keywords
        
        # Simple keyword extraction (in production, use NLP)
        description = description.lower()
        
        features = {
            "face_shape": "oval",
            "skin_tone": "medium",
            "hair_color": "brown",
            "hair_style": "short",
            "eye_color": "brown",
            "facial_features": {
                "eyes": "round",
                "nose": "medium",
                "mouth": "medium"
            }
        }
        
        # Very basic keyword matching (for demonstration)
        if "blonde" in description or "yellow hair" in description:
            features["hair_color"] = "blonde"
        if "blue eyes" in description:
            features["eye_color"] = "blue"
        if "long hair" in description:
            features["hair_style"] = "long"
        
        return {
            "source_type": "description",
            "style": style,
            "description": description,
            "features": features
        }
    
    def _generate_default_avatar(self, style: str) -> Dict[str, Any]:
        """
        Generates default avatar features when no input is provided.
        """
        return {
            "source_type": "default",
            "style": style,
            "features": {
                "face_shape": "oval",
                "skin_tone": "medium",
                "hair_color": "brown",
                "hair_style": "short",
                "eye_color": "brown",
                "facial_features": {
                    "eyes": "round",
                    "nose": "medium",
                    "mouth": "medium"
                }
            }
        }
