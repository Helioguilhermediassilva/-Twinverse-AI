# Twinverse-AI: Technical Documentation

## Project Overview

Twinverse-AI is a multimodal AI platform that transforms creative phrases into complete artistic experiences through four integrated phases:

1. **Music Generation**: Creates original music from a creative phrase
2. **Avatar Generation**: Produces a digital avatar synchronized with the music
3. **Short Film Creation**: Generates a narrative short film featuring the avatar
4. **Publication**: Compiles all assets into a shareable web page

This document provides technical documentation for the expanded platform, focusing on the newly added phases (avatar, film, and publication).

## System Architecture

The Twinverse-AI platform follows a modular architecture with clear separation between phases:

```
+---------------------+     +---------------------+     +---------------------+
|                     |     |                     |     |                     |
|  Client Application |<--->|  Backend Services   |<--->|   External APIs     |
|  (React)            |     |  (FastAPI)          |     |                     |
|                     |     |                     |     |                     |
+---------------------+     +---------------------+     +---------------------+
                                      ^
                                      |
                                      v
                            +---------------------+
                            |                     |
                            |  Asset Storage      |
                            |                     |
                            +---------------------+
```

### Backend Architecture

The backend is built with FastAPI and organized into service modules:

#### Core Services
- Configuration Management
- Authentication & Authorization
- Middleware & Utilities
- API Gateway

#### Phase-Specific Services

**Music Generation (Existing)**
- Phrase Interpreter Service
- Lyrics Generator Service
- Music Generator Service
- Voice Processor Service

**Avatar Generation (New)**
- Visual Description Processor
- Avatar Creator Service
- Animation Synchronizer Service
- 3D Model Exporter Service

**Short Film (New)**
- Screenplay Generator Service
- Storyboard Creator Service
- Video Generation Service
- Video Editor Service

**Publication (New)**
- Page Template Service
- Asset Compiler Service
- URL Generator Service
- Sharing Integration Service

### Frontend Architecture

The frontend is built with React and organized into components and pages:

#### Core Components
- Routing System
- State Management
- API Client
- Authentication

#### Phase-Specific Interfaces

**Music Creation**
- Phrase Input Form
- Music Player
- Voice Upload

**Avatar Creation**
- Visual Description Form
- Image Upload
- Style Selector
- Avatar Previewer (WebGL)

**Short Film**
- Screenplay Viewer
- Storyboard Viewer
- Video Player
- Generation Progress Tracker

**Publication**
- Experience Preview
- Sharing Controls
- URL Display
- Download Options

## API Reference

### Avatar API Endpoints

#### POST /api/avatar/create
Creates a digital avatar based on visual description or uploaded image.

**Parameters:**
- `music_id` (required): ID of the previously created music
- `visual_description` (optional): Textual description of desired avatar appearance
- `style` (optional): Visual style (realistic, cartoon, anime, futuristic)
- `image_file` (optional): User's selfie or reference image

**Response:**
```json
{
  "id": "avatar_123_abc",
  "music_id": "music_123",
  "avatar_video_url": "/api/avatar/avatar_123_abc/video",
  "avatar_model_url": "/api/avatar/avatar_123_abc/model",
  "status": "processing"
}
```

#### GET /api/avatar/{avatar_id}
Checks the status of avatar generation.

**Response:**
```json
{
  "id": "avatar_123_abc",
  "status": "completed",
  "avatar_video_url": "/api/avatar/avatar_123_abc/video",
  "avatar_model_url": "/api/avatar/avatar_123_abc/model"
}
```

#### GET /api/avatar/{avatar_id}/video
Returns the avatar video file for streaming.

#### GET /api/avatar/{avatar_id}/model
Returns the 3D model file of the avatar.

### Film API Endpoints

#### POST /api/film/create
Creates a short film based on music and avatar.

**Parameters:**
- `music_id` (required): ID of the previously created music
- `avatar_id` (required): ID of the previously created avatar

**Response:**
```json
{
  "id": "film_123_abc",
  "music_id": "music_123",
  "avatar_id": "avatar_123_abc",
  "screenplay_url": "/api/film/film_123_abc/screenplay",
  "storyboard_url": "/api/film/film_123_abc/storyboard",
  "film_url": "/api/film/film_123_abc/video",
  "status": "processing"
}
```

#### GET /api/film/{film_id}
Checks the status of film generation.

**Response:**
```json
{
  "id": "film_123_abc",
  "status": "completed",
  "screenplay_url": "/api/film/film_123_abc/screenplay",
  "storyboard_url": "/api/film/film_123_abc/storyboard",
  "film_url": "/api/film/film_123_abc/video"
}
```

#### GET /api/film/{film_id}/video
Returns the film video file for streaming.

#### GET /api/film/{film_id}/screenplay
Returns the screenplay text file.

#### GET /api/film/{film_id}/storyboard
Returns the storyboard image file.

### Publication API Endpoints

#### POST /api/publication/create
Creates a publication page with all generated content.

**Parameters:**
- `music_id` (required): ID of the previously created music
- `avatar_id` (required): ID of the previously created avatar
- `film_id` (required): ID of the previously created film
- `artist_name` (optional): Artist name or character name

**Response:**
```json
{
  "id": "pub_123_abc",
  "music_id": "music_123",
  "avatar_id": "avatar_123_abc",
  "film_id": "film_123_abc",
  "public_url": "https://www.twinversestudios.cloud/user_xyz",
  "status": "processing"
}
```

#### GET /api/publication/{publication_id}
Checks the status of publication generation.

**Response:**
```json
{
  "id": "pub_123_abc",
  "status": "completed",
  "public_url": "https://www.twinversestudios.cloud/user_xyz",
  "html_url": "/api/publication/pub_123_abc/html"
}
```

#### GET /api/publication/{publication_id}/html
Returns the HTML file of the publication page.

## Service Implementations

### Avatar Generation Services

#### VisualProcessorService
Processes visual input (description or image) to extract features for avatar creation.

**Key Methods:**
- `process(description, image_file, style)`: Processes visual input and returns features

#### AvatarCreatorService
Creates base avatars using Ready Player Me or similar avatar creation APIs.

**Key Methods:**
- `create(visual_data, style, output_dir)`: Creates a base avatar using visual data

#### AnimationSynchronizerService
Synchronizes avatar animations with music.

**Key Methods:**
- `synchronize(avatar_base, music_path, output_dir)`: Synchronizes avatar with music

#### ModelExporterService
Exports animated avatars as video and 3D model files.

**Key Methods:**
- `export(animated_avatar, formats, output_dir)`: Exports avatar in multiple formats

### Film Creation Services

#### ScreenplayGeneratorService
Generates screenplays for short films based on music and avatar.

**Key Methods:**
- `generate(music_id, avatar_id, output_path)`: Generates a screenplay

#### StoryboardCreatorService
Creates storyboards based on screenplays.

**Key Methods:**
- `create(screenplay, output_path)`: Creates a storyboard with key scenes

#### VideoGeneratorService
Generates video scenes based on screenplay and storyboard.

**Key Methods:**
- `generate(screenplay, storyboard, output_dir)`: Generates video scenes

#### VideoEditorService
Edits the final short film by combining scenes, music, and avatar.

**Key Methods:**
- `edit(scenes, music_path, avatar_path, output_path)`: Edits the final film

### Publication Services

#### AssetCompilerService
Compiles assets from all previous phases for use in the publication page.

**Key Methods:**
- `compile(music_id, avatar_id, film_id, output_dir)`: Compiles all assets

#### PageTemplateService
Generates publication page templates that showcase all created content.

**Key Methods:**
- `generate(assets, artist_name, output_path)`: Generates HTML page

#### URLGeneratorService
Generates public URLs for publication pages.

**Key Methods:**
- `generate(user_id, publication_id)`: Generates a public URL

#### SharingIntegrationService
Sets up social media sharing integrations for the publication page.

**Key Methods:**
- `setup(publication_id, public_url, assets)`: Sets up sharing integrations

## Frontend Components

### Avatar Components

#### VisualDescriptionForm
Form for entering textual description of desired avatar appearance.

#### ImageUploader
Component for uploading selfie or reference image.

#### AvatarStyleSelector
Selector for choosing avatar visual style (realistic, cartoon, anime, futuristic).

#### AvatarPreview
Component for previewing the generated avatar.

### Film Components

#### FilmPlayer
Video player for the generated short film.

#### ScreenplayViewer
Component for viewing the generated screenplay.

#### StoryboardViewer
Component for viewing the generated storyboard.

### Publication Components

#### PublicationViewer
Component for previewing the publication page.

#### SharingButtons
Buttons for sharing the publication on social media.

## Data Flow

The system maintains a unidirectional data flow:

1. User enters creative phrase → Music is generated
2. User provides visual input → Avatar is created and synchronized with music
3. System generates film using avatar and music
4. System compiles all assets into publication page with sharing options

## External API Integrations

### Avatar Generation
- Ready Player Me: Base avatar creation
- OpenAI DALL-E 3: Visual style application
- Three.js: 3D rendering and animation

### Short Film Creation
- OpenAI GPT-4o: Screenplay generation
- Runway ML Gen-2 / Pika Labs: Video generation
- FFmpeg: Video processing and editing

### Publication
- Vercel / Netlify: Page hosting and deployment
- Social Media APIs: Sharing functionality
- CDN Services: Media delivery

## Installation and Setup

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment variables:
```
OPENAI_API_KEY=your_openai_key
READY_PLAYER_ME_API_KEY=your_rpm_key
RUNWAY_API_KEY=your_runway_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

3. Start the server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend/twinverse-ui
npm install
```

2. Configure API endpoint:
Edit `.env` file to point to your backend server.

3. Start development server:
```bash
npm run dev
```

## Deployment

The system can be deployed using Docker containers:

1. Build backend image:
```bash
docker build -t twinverse-backend ./backend
```

2. Build frontend image:
```bash
docker build -t twinverse-frontend ./frontend/twinverse-ui
```

3. Deploy with docker-compose:
```bash
docker-compose up -d
```

## Security Considerations

- API keys are stored in environment variables
- User authentication is required for creating content
- Content moderation is applied to user inputs
- Rate limiting prevents API abuse
- CORS configuration restricts access to approved domains

## Performance Optimization

- Asynchronous processing for long-running tasks
- Task queues for background processing
- Caching for frequently accessed assets
- CDN for media delivery
- Optimized media formats for web delivery

## Future Enhancements

- Enhanced avatar emotion mapping from music
- Advanced video scene transitions and effects
- Additional social media integration
- Analytics for tracking publication views and shares
- Mobile app version

## Conclusion

The Twinverse-AI platform provides a comprehensive solution for transforming creative phrases into complete artistic experiences. The modular architecture allows for easy maintenance and future expansion, while the integration with cutting-edge AI services ensures high-quality output across all phases.
