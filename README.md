# EcoSort AI - Smart Waste Classification & Disposal Guidance System for India

EcoSort AI is a production-grade, AI-powered waste management ecosystem designed for citizens, municipalities, institutions (schools/colleges), NGOs, and recycling companies in India.

---

## System Architecture Overview

EcoSort AI is built on a clean, scalable architecture:
- **Backend API**: FastAPI (Python 3.11) with Motor (Async MongoDB), Redis, Pydantic v2, and JWT authentication.
- **AI Inference Engine**: MobileNetV3 / EfficientNet deep learning model exported to TensorFlow Lite (.tflite) for edge mobile execution and cloud API fallback.
- **Mobile Application**: React Native (Android) with offline TFLite scan capabilities and localization (English & Hindi).
- **Web Dashboard**: React 18 + Vite + Tailwind CSS for municipal analytics, scrap vendor pickup management, and institutional waste audits.
- **Database**: MongoDB Atlas document store with 2dsphere spatial indexing for Google Maps recycling center proximity.

---

## Repository Structure

```
ecosort-ai/
├── infrastructure/
│   └── docker/                  # Container Dockerfiles & docker-compose
├── packages/
│   ├── ai-engine/               # PyTorch training & TFLite quantization
│   ├── backend-api/             # FastAPI REST API Backend
│   ├── mobile-app/              # React Native Android App
│   └── web-dashboard/           # React 18 Web SPA Dashboard
├── shared/
│   └── types/                   # Shared TypeScript Interfaces
└── docs/                        # Specifications & Architecture Docs
```

---

## Quick Start (Sprint 1 Foundation)

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Docker Engine & Docker Compose
- MongoDB (Local instance or MongoDB Atlas URI)
- Redis

### 1. Environment Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 2. Run Backend API via Docker Compose
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up --build
```
The FastAPI backend server will be running at `http://localhost:8000`. Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

### Production MongoDB Configuration

Production requires a reachable MongoDB deployment. MongoDB Atlas is recommended:

1. Create an Atlas cluster and database user.
2. Add the deployment IP to the Atlas network access list.
3. Set these backend environment variables in the production host:

```env
APP_ENV=production
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=ecosort_db
SECRET_KEY=<long-random-secret>
```

The backend now fails startup when production MongoDB is unreachable instead of serving requests with missing persistence. Verify the connection with `GET /api/v1/health` after deployment; its MongoDB service must report `healthy`.

### 3. Run Web Dashboard Locally
```bash
cd packages/web-dashboard
npm install
npm run dev
```
The Web Dashboard will be running at `http://localhost:5173`.

### 4. Run Mobile App (React Native)
```bash
cd packages/mobile-app
npm install
npm run start
```

---

## License
Proprietary / Open Academic License - Developed for EcoSort AI Initiative India.
