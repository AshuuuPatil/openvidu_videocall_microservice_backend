from fastapi import FastAPI, Depends
from app.routers import auth
from app.dependencies import verify_token
from fastapi.middleware.cors import CORSMiddleware

from app.services.openvidu_service import OpenViduService
from app.routers import video

app = FastAPI(
title="OpenVidu FastAPI POC",
version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(video.router)

@app.get("/")
def root():
    return {"message": "OpenVidu FastAPI POC running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {"message": "Protected route accessed", "user": user}

@app.get("/test-openvidu")
def test_openvidu():
    session = OpenViduService.create_session("poc-test-session")
    return session