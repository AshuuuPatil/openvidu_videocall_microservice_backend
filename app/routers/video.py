from fastapi import APIRouter, Depends, HTTPException
from app.schemas.video_schema import VideoSessionRequest, VideoSessionResponse
from app.services.openvidu_service import OpenViduService
from app.dependencies import verify_token
from app.config import settings

router = APIRouter(prefix="/api/video", tags=["Video"])

@router.post("/session", response_model=VideoSessionResponse)
def create_video_session(
request: VideoSessionRequest,
user=Depends(verify_token)
):
    try:
        # Create session if not exists
        OpenViduService.create_session(request.session_id)
            
        # Create connection token
        connection = OpenViduService.create_connection(request.session_id)

        return VideoSessionResponse(
            sessionId=request.session_id,
            token=connection["token"],
            openviduUrl=settings.OPENVIDU_URL
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))