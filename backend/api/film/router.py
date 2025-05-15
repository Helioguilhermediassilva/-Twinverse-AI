from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from typing import Optional
import os
from pydantic import BaseModel

# Import services
from services.film.screenplay_generator import ScreenplayGeneratorService
from services.film.storyboard_creator import StoryboardCreatorService
from services.film.video_generator import VideoGeneratorService
from services.film.video_editor import VideoEditorService

router = APIRouter(tags=["film"])

# Data models
class FilmRequest(BaseModel):
    music_id: str
    avatar_id: str
    
class FilmResponse(BaseModel):
    id: str
    music_id: str
    avatar_id: str
    screenplay_url: str
    storyboard_url: str
    film_url: str
    status: str

# Endpoints
@router.post("/film/create", response_model=FilmResponse)
async def create_film(
    music_id: str = Form(...),
    avatar_id: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Creates a short film based on music and avatar.
    
    - **music_id**: ID of the previously created music
    - **avatar_id**: ID of the previously created avatar
    """
    try:
        # Generate unique ID for the film
        film_id = f"film_{music_id}_{avatar_id}_{os.urandom(4).hex()}"
        
        # Start film generation process in background
        background_tasks.add_task(
            process_film_generation,
            film_id=film_id,
            music_id=music_id,
            avatar_id=avatar_id
        )
        
        return {
            "id": film_id,
            "music_id": music_id,
            "avatar_id": avatar_id,
            "screenplay_url": f"/api/film/{film_id}/screenplay",
            "storyboard_url": f"/api/film/{film_id}/storyboard",
            "film_url": f"/api/film/{film_id}/video",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating film: {str(e)}")

@router.get("/film/{film_id}")
async def get_film_status(film_id: str):
    """
    Checks the status of film generation.
    """
    # Check if film exists and its status
    # Simplified implementation - in production, would check database
    film_path = f"./storage/film/{film_id}/curta_twinverse.mp4"
    screenplay_path = f"./storage/film/{film_id}/roteiro_curta.txt"
    
    if os.path.exists(film_path) and os.path.exists(screenplay_path):
        return {
            "id": film_id,
            "status": "completed",
            "screenplay_url": f"/api/film/{film_id}/screenplay",
            "storyboard_url": f"/api/film/{film_id}/storyboard",
            "film_url": f"/api/film/{film_id}/video"
        }
    else:
        return {
            "id": film_id,
            "status": "processing"
        }

@router.get("/film/{film_id}/video")
async def stream_film(film_id: str):
    """
    Returns the film video file for streaming.
    """
    from fastapi.responses import FileResponse
    
    film_path = f"./storage/film/{film_id}/curta_twinverse.mp4"
    
    if not os.path.exists(film_path):
        raise HTTPException(status_code=404, detail="Film not found or still processing")
    
    return FileResponse(
        path=film_path,
        media_type="video/mp4",
        filename=f"twinverse_film_{film_id}.mp4"
    )

@router.get("/film/{film_id}/screenplay")
async def get_screenplay(film_id: str):
    """
    Returns the screenplay text file.
    """
    from fastapi.responses import FileResponse
    
    screenplay_path = f"./storage/film/{film_id}/roteiro_curta.txt"
    
    if not os.path.exists(screenplay_path):
        raise HTTPException(status_code=404, detail="Screenplay not found or still processing")
    
    return FileResponse(
        path=screenplay_path,
        media_type="text/plain",
        filename=f"twinverse_screenplay_{film_id}.txt"
    )

@router.get("/film/{film_id}/storyboard")
async def get_storyboard(film_id: str):
    """
    Returns the storyboard image file.
    """
    from fastapi.responses import FileResponse
    
    storyboard_path = f"./storage/film/{film_id}/storyboard.jpg"
    
    if not os.path.exists(storyboard_path):
        raise HTTPException(status_code=404, detail="Storyboard not found or still processing")
    
    return FileResponse(
        path=storyboard_path,
        media_type="image/jpeg",
        filename=f"twinverse_storyboard_{film_id}.jpg"
    )

# Background processing function
async def process_film_generation(
    film_id: str,
    music_id: str,
    avatar_id: str
):
    try:
        # Create directory for film files
        os.makedirs(f"./storage/film/{film_id}", exist_ok=True)
        
        # Get music and avatar data
        # In production, would retrieve from database
        music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
        avatar_video_path = f"./storage/avatar/{avatar_id}/avatar_video.mp4"
        
        # Generate screenplay
        screenplay_generator = ScreenplayGeneratorService()
        screenplay = await screenplay_generator.generate(
            music_id=music_id,
            avatar_id=avatar_id,
            output_path=f"./storage/film/{film_id}/roteiro_curta.txt"
        )
        
        # Create storyboard
        storyboard_creator = StoryboardCreatorService()
        storyboard = await storyboard_creator.create(
            screenplay=screenplay,
            output_path=f"./storage/film/{film_id}/storyboard.jpg"
        )
        
        # Generate video scenes
        video_generator = VideoGeneratorService()
        scenes = await video_generator.generate(
            screenplay=screenplay,
            storyboard=storyboard,
            output_dir=f"./storage/film/{film_id}/scenes"
        )
        
        # Edit final film
        video_editor = VideoEditorService()
        final_film = await video_editor.edit(
            scenes=scenes,
            music_path=music_path,
            avatar_path=avatar_video_path,
            output_path=f"./storage/film/{film_id}/curta_twinverse.mp4"
        )
        
        # In production, would update status in database
        
    except Exception as e:
        # Log error and update status
        with open(f"./storage/film/{film_id}/error.log", "w") as f:
            f.write(f"Error generating film: {str(e)}")
