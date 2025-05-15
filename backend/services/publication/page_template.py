import os
from typing import Dict, Any, List, Optional
from core.config import settings

class PageTemplateService:
    """
    Service responsible for generating publication page templates
    that showcase all created content (music, avatar, film).
    """
    
    def __init__(self):
        pass
        
    async def generate(
        self,
        assets: Dict[str, Any],
        artist_name: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a publication page template with all assets.
        
        Args:
            assets: Dictionary containing compiled assets
            artist_name: Optional artist or character name
            output_path: Path to save the HTML file
            
        Returns:
            Dictionary containing page information
        """
        try:
            # Create output directory if needed
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Use default artist name if not provided
            if not artist_name:
                artist_name = "Twinverse Artist"
            
            # Get creative phrase from assets
            creative_phrase = assets.get("phrase", "Creative Expression")
            
            # Generate HTML content
            html_content = self._generate_html_template(
                artist_name=artist_name,
                creative_phrase=creative_phrase,
                assets=assets
            )
            
            # Save HTML to file if output path provided
            if output_path:
                with open(output_path, "w") as f:
                    f.write(html_content)
            
            return {
                "html_content": html_content,
                "artist_name": artist_name,
                "creative_phrase": creative_phrase,
                "file_path": output_path
            }
                
        except Exception as e:
            print(f"Error generating page template: {str(e)}")
            # Generate basic page in case of error
            return self._generate_basic_page(assets, artist_name, output_path)
    
    def _generate_html_template(
        self,
        artist_name: str,
        creative_phrase: str,
        assets: Dict[str, Any]
    ) -> str:
        """
        Generates HTML content for the publication page.
        """
        # Get asset paths
        music_url = assets.get("music_url", "#")
        avatar_url = assets.get("avatar_url", "#")
        film_url = assets.get("film_url", "#")
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{artist_name} - Twinverse Experience</title>
    <style>
        :root {{
            --primary-color: #8b5cf6;
            --secondary-color: #3b82f6;
            --background-color: #f9fafb;
            --text-color: #1f2937;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        header {{
            background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem 1rem;
            text-align: center;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .creative-phrase {{
            font-style: italic;
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background-color: rgba(139, 92, 246, 0.1);
            border-radius: 0.5rem;
        }}
        
        .section {{
            margin-bottom: 3rem;
            padding: 2rem;
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .section-title {{
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            color: var(--primary-color);
        }}
        
        .music-player {{
            width: 100%;
            margin-bottom: 1rem;
        }}
        
        .avatar-container {{
            display: flex;
            justify-content: center;
            margin-bottom: 1rem;
        }}
        
        .film-container {{
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
            max-width: 100%;
        }}
        
        .film-container video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
        
        .sharing-buttons {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .sharing-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: white;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.2s;
        }}
        
        .sharing-button:hover {{
            background-color: var(--secondary-color);
        }}
        
        footer {{
            text-align: center;
            padding: 2rem 1rem;
            background-color: var(--text-color);
            color: white;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{artist_name}</h1>
        <p>A Twinverse AI Experience</p>
    </header>
    
    <div class="container">
        <div class="creative-phrase">
            "{creative_phrase}"
        </div>
        
        <div class="section">
            <h2 class="section-title">Original Music</h2>
            <audio class="music-player" controls src="{music_url}">
                Your browser does not support the audio element.
            </audio>
            <p>Listen to the original music created from the creative phrase.</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">Digital Avatar</h2>
            <div class="avatar-container">
                <video width="320" height="240" controls>
                    <source src="{avatar_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <p>Meet the digital avatar created to embody the essence of the music.</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">Short Film</h2>
            <div class="film-container">
                <video controls>
                    <source src="{film_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            <p>Experience the complete artistic journey through this short film.</p>
        </div>
        
        <div class="sharing-buttons">
            <a href="#" class="sharing-button">Share on YouTube</a>
            <a href="#" class="sharing-button">Share on TikTok</a>
            <a href="#" class="sharing-button">Share on Spotify</a>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2024 Twinverse Studios. All rights reserved.</p>
        <p>Created with Twinverse AI</p>
    </footer>
</body>
</html>
"""
    
    def _generate_basic_page(
        self,
        assets: Dict[str, Any],
        artist_name: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a basic page when normal generation fails.
        """
        # Use default artist name if not provided
        if not artist_name:
            artist_name = "Twinverse Artist"
        
        # Get creative phrase from assets
        creative_phrase = assets.get("phrase", "Creative Expression")
        
        # Generate basic HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{artist_name} - Twinverse Experience</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        h1 {{
            color: purple;
        }}
    </style>
</head>
<body>
    <h1>{artist_name}</h1>
    <p>"{creative_phrase}"</p>
    <p>This is a basic Twinverse experience page.</p>
    <p>Music, avatar, and film will be available soon.</p>
</body>
</html>
"""
        
        # Save HTML to file if output path provided
        if output_path:
            with open(output_path, "w") as f:
                f.write(html_content)
        
        return {
            "html_content": html_content,
            "artist_name": artist_name,
            "creative_phrase": creative_phrase,
            "file_path": output_path
        }
