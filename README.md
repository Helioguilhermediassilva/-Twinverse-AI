# Twinverse-AI

## Multimodal AI Platform for Creative Expression

Twinverse-AI is an advanced AI platform that transforms creative phrases into complete artistic experiences through four integrated phases:

1. **Music Generation**: Creates original music from a creative phrase
2. **Avatar Generation**: Produces a digital avatar synchronized with the music
3. **Short Film Creation**: Generates a narrative short film featuring the avatar
4. **Publication**: Compiles all assets into a shareable web page

## Features

### Music Generation
- Creative phrase analysis for emotion and theme extraction
- Original lyrics generation with structured verses and chorus
- Melody composition matching the emotional tone
- Voice integration (user-provided or AI-generated)

### Avatar Generation
- Multiple visual styles (realistic, cartoon, anime, futuristic)
- Creation from textual descriptions or reference images
- Lip-syncing and emotional expression synchronized with music
- Export as video and 3D model formats

### Short Film Creation
- Three-act screenplay generation based on music narrative
- Automatic storyboard creation for key scenes
- AI-powered video scene generation
- Professional editing with avatar integration

### Publication
- Personalized web page showcasing all created content
- Public URL generation for easy sharing
- Social media integration (YouTube, TikTok, Spotify)
- Responsive design for all devices

## Technology Stack

### Backend
- Python 3.9+
- FastAPI
- Pydantic
- OpenAI (GPT-4o)
- Ready Player Me API
- Runway ML / Pika Labs

### Frontend
- React 18
- Vite
- React Router
- Tailwind CSS
- Three.js for 3D rendering

## Project Structure

```
Twinverse-AI/
├── backend/                  # FastAPI backend
│   ├── api/                  # API endpoints
│   │   ├── avatar/           # Avatar generation endpoints
│   │   ├── film/             # Film creation endpoints
│   │   └── publication/      # Publication endpoints
│   ├── core/                 # Core configurations
│   ├── models/               # Data models
│   ├── repositories/         # Data access
│   ├── services/             # Business logic
│   │   ├── avatar/           # Avatar generation services
│   │   ├── film/             # Film creation services
│   │   └── publication/      # Publication services
│   └── main.py               # Application entry point
├── frontend/                 # React frontend
│   └── twinverse-ui/         # React application
│       ├── public/           # Static assets
│       └── src/              # Source code
│           ├── components/   # Reusable components
│           ├── pages/        # Application pages
│           ├── services/     # API clients
│           └── utils/        # Utilities
├── prompts/                  # AI prompts
├── characters/               # Character resources
├── media/                    # Media resources
└── docs/                     # Documentation
```

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

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

2. Start development server:
```bash
npm run dev
```

## User Flow

1. **Music Creation**:
   - Enter a creative phrase
   - Optionally specify genre and emotion
   - Optionally provide voice recording
   - Receive generated music

2. **Avatar Creation**:
   - Choose visual style
   - Provide description or upload image
   - Receive avatar synchronized with music

3. **Film Creation**:
   - System automatically generates screenplay
   - Creates storyboard and video scenes
   - Combines with avatar and music

4. **Publication**:
   - System compiles all assets
   - Generates public URL
   - Provides sharing options

## API Documentation

The API documentation is available at `/docs` when running the backend server.

## Deployment

### Docker Deployment

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

### Cloud Deployment

The application can be deployed to any cloud provider that supports Docker containers or Python/Node.js applications.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT models
- Ready Player Me for avatar technology
- Runway ML and Pika Labs for video generation capabilities

## Contact

For questions or support, please contact support@twinversestudios.com
