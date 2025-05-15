from fastapi import APIRouter, HTTPException, Depends, Form, BackgroundTasks
from typing import Optional
import os
from pydantic import BaseModel

# Import services
from services.publication.page_template import PageTemplateService
from services.publication.asset_compiler import AssetCompilerService
from services.publication.url_generator import URLGeneratorService
from services.publication.sharing_integration import SharingIntegrationService

router = APIRouter(tags=["publication"])

# Data models
class PublicationRequest(BaseModel):
    music_id: str
    avatar_id: str
    film_id: str
    artist_name: Optional[str] = None
    
class PublicationResponse(BaseModel):
    id: str
    music_id: str
    avatar_id: str
    film_id: str
    public_url: str
    status: str

# Endpoints
@router.post("/publication/create", response_model=PublicationResponse)
async def create_publication(
    music_id: str = Form(...),
    avatar_id: str = Form(...),
    film_id: str = Form(...),
    artist_name: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Creates a publication page with all generated content.
    
    - **music_id**: ID of the previously created music
    - **avatar_id**: ID of the previously created avatar
    - **film_id**: ID of the previously created film
    - **artist_name**: (Optional) Artist name or character name
    """
    try:
        # Generate unique ID for the publication
        publication_id = f"pub_{music_id}_{os.urandom(4).hex()}"
        
        # Generate user ID for URL
        user_id = f"user_{os.urandom(8).hex()}"
        
        # Start publication generation process in background
        background_tasks.add_task(
            process_publication_generation,
            publication_id=publication_id,
            music_id=music_id,
            avatar_id=avatar_id,
            film_id=film_id,
            artist_name=artist_name,
            user_id=user_id
        )
        
        return {
            "id": publication_id,
            "music_id": music_id,
            "avatar_id": avatar_id,
            "film_id": film_id,
            "public_url": f"https://www.twinversestudios.cloud/{user_id}",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating publication: {str(e)}")

@router.get("/publication/{publication_id}")
async def get_publication_status(publication_id: str):
    """
    Checks the status of publication generation.
    """
    # Check if publication exists and its status
    # Simplified implementation - in production, would check database
    publication_path = f"./storage/publication/{publication_id}/pagina_publicacao.html"
    
    if os.path.exists(publication_path):
        # In production, would retrieve from database
        user_id = publication_id.replace("pub_", "user_")
        
        return {
            "id": publication_id,
            "status": "completed",
            "public_url": f"https://www.twinversestudios.cloud/{user_id}",
            "html_url": f"/api/publication/{publication_id}/html"
        }
    else:
        return {
            "id": publication_id,
            "status": "processing"
        }

@router.get("/publication/{publication_id}/html")
async def get_publication_html(publication_id: str):
    """
    Returns the HTML file of the publication page.
    """
    from fastapi.responses import FileResponse
    
    publication_path = f"./storage/publication/{publication_id}/pagina_publicacao.html"
    
    if not os.path.exists(publication_path):
        raise HTTPException(status_code=404, detail="Publication not found or still processing")
    
    return FileResponse(
        path=publication_path,
        media_type="text/html",
        filename=f"twinverse_publication_{publication_id}.html"
    )

# Background processing function
async def process_publication_generation(
    publication_id: str,
    music_id: str,
    avatar_id: str,
    film_id: str,
    artist_name: Optional[str],
    user_id: str
):
    try:
        # Create directory for publication files
        os.makedirs(f"./storage/publication/{publication_id}", exist_ok=True)
        
        # Compile assets from previous phases
        asset_compiler = AssetCompilerService()
        assets = await asset_compiler.compile(
            music_id=music_id,
            avatar_id=avatar_id,
            film_id=film_id,
            output_dir=f"./storage/publication/{publication_id}/assets"
        )
        
        # Generate page template
        page_template = PageTemplateService()
        page = await page_template.generate(
            assets=assets,
            artist_name=artist_name,
            output_path=f"./storage/publication/{publication_id}/pagina_publicacao.html"
        )
        
        # Generate public URL
        url_generator = URLGeneratorService()
        url = await url_generator.generate(
            user_id=user_id,
            publication_id=publication_id
        )
        
        # Set up sharing integrations
        sharing_integration = SharingIntegrationService()
        sharing = await sharing_integration.setup(
            publication_id=publication_id,
            public_url=url,
            assets=assets
        )
        
        # In production, would update status in database
        
    except Exception as e:
        # Log error and update status
        with open(f"./storage/publication/{publication_id}/error.log", "w") as f:
            f.write(f"Error generating publication: {str(e)}")
