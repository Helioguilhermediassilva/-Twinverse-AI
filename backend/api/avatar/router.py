from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form, BackgroundTasks
from typing import Optional
import os
from pydantic import BaseModel

# Import services
from services.avatar.visual_processor import VisualProcessorService
from services.avatar.avatar_creator import AvatarCreatorService
from services.avatar.animation_synchronizer import AnimationSynchronizerService
from services.avatar.model_exporter import ModelExporterService

router = APIRouter(tags=["avatar"])

# Data models
class AvatarRequest(BaseModel):
    music_id: str
    visual_description: Optional[str] = None
    style: str = "realistic"  # realistic, cartoon, anime, futuristic
    
class AvatarResponse(BaseModel):
    id: str
    music_id: str
    avatar_video_url: str
    avatar_model_url: str
    status: str

# Endpoints
@router.post("/avatar/create", response_model=AvatarResponse)
async def create_avatar(
    music_id: str = Form(...),
    visual_description: Optional[str] = Form(None),
    style: str = Form("realistic"),
    image_file: Optional[UploadFile] = File(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Creates a digital avatar based on visual description or uploaded image.
    
    - **music_id**: ID of the previously created music
    - **visual_description**: (Optional) Textual description of desired avatar appearance
    - **style**: Visual style (realistic, cartoon, anime, futuristic)
    - **image_file**: (Optional) User's selfie or reference image
    """
    try:
        # Generate unique ID for the avatar
        avatar_id = f"avatar_{music_id}_{os.urandom(4).hex()}"
        
        # Process visual input (description or image)
        visual_processor = VisualProcessorService()
        visual_data = await visual_processor.process(
            description=visual_description,
            image_file=image_file,
            style=style
        )
        
        # Start avatar generation process in background
        background_tasks.add_task(
            process_avatar_generation,
            avatar_id=avatar_id,
            music_id=music_id,
            visual_data=visual_data,
            style=style
        )
        
        return {
            "id": avatar_id,
            "music_id": music_id,
            "avatar_video_url": f"/api/avatar/{avatar_id}/video",
            "avatar_model_url": f"/api/avatar/{avatar_id}/model",
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating avatar: {str(e)}")

@router.get("/avatar/{avatar_id}")
async def get_avatar_status(avatar_id: str):
    """
    Checks the status of avatar generation.
    """
    # Check if avatar exists and its status
    # Simplified implementation - in production, would check database
    avatar_video_path = f"./storage/avatar/{avatar_id}/avatar_video.mp4"
    avatar_model_path = f"./storage/avatar/{avatar_id}/avatar_model.glb"
    
    if os.path.exists(avatar_video_path) and os.path.exists(avatar_model_path):
        return {
            "id": avatar_id,
            "status": "completed",
            "avatar_video_url": f"/api/avatar/{avatar_id}/video",
            "avatar_model_url": f"/api/avatar/{avatar_id}/model"
        }
    else:
        return {
            "id": avatar_id,
            "status": "processing"
        }

@router.get("/avatar/{avatar_id}/video")
async def stream_avatar_video(avatar_id: str):
    """
    Returns the avatar video file for streaming.
    """
    from fastapi.responses import FileResponse
    
    avatar_path = f"./storage/avatar/{avatar_id}/avatar_video.mp4"
    
    if not os.path.exists(avatar_path):
        raise HTTPException(status_code=404, detail="Avatar video not found or still processing")
    
    return FileResponse(
        path=avatar_path,
        media_type="video/mp4",
        filename=f"twinverse_avatar_{avatar_id}.mp4"
    )

@router.get("/avatar/{avatar_id}/model")
async def download_avatar_model(avatar_id: str):
    """
    Returns the 3D model file of the avatar.
    """
    from fastapi.responses import FileResponse
    
    model_path = f"./storage/avatar/{avatar_id}/avatar_model.glb"
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Avatar model not found or still processing")
    
    return FileResponse(
        path=model_path,
        media_type="model/gltf-binary",
        filename=f"twinverse_avatar_{avatar_id}.glb"
    )

# Background processing function
async def process_avatar_generation(
    avatar_id: str,
    music_id: str,
    visual_data: dict,
    style: str
):
    try:
        # Create directory for avatar files
        os.makedirs(f"./storage/avatar/{avatar_id}", exist_ok=True)
        
        # Get music data for emotion and voice characteristics
        # In production, would retrieve from database
        music_path = f"./storage/music/{music_id}/musica_finalizada.mp3"
        
        # Create base avatar
        avatar_creator = AvatarCreatorService()
        avatar_base = await avatar_creator.create(
            visual_data=visual_data,
            style=style,
            output_dir=f"./storage/avatar/{avatar_id}"
        )
        
        # Synchronize avatar with music
        animation_synchronizer = AnimationSynchronizerService()
        animated_avatar = await animation_synchronizer.synchronize(
            avatar_base=avatar_base,
            music_path=music_path,
            output_dir=f"./storage/avatar/{avatar_id}"
        )
        
        # Export avatar as video and 3D model
        model_exporter = ModelExporterService()
        await model_exporter.export(
            animated_avatar=animated_avatar,
            formats=["mp4", "glb"],
            output_dir=f"./storage/avatar/{avatar_id}"
        )
        
        # In production, would update status in database
        
    except Exception as e:
        # Log error and update status
        with open(f"./storage/avatar/{avatar_id}/error.log", "w") as f:
            f.write(f"Error generating avatar: {str(e)}")
