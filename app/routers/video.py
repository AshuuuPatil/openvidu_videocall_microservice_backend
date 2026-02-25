from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.schemas.video_schema import VideoSessionRequest, VideoSessionResponse
from app.services.openvidu_service import OpenViduService
from app.dependencies import verify_token
from app.config import settings
import httpx

router = APIRouter(prefix="/api/video", tags=["Video"])

@router.post("/session", response_model=VideoSessionResponse)
def create_video_session(
    request: VideoSessionRequest,
    user=Depends(verify_token)
):
    try:
        OpenViduService.create_session(request.session_id)
        connection = OpenViduService.create_connection(request.session_id)
        return VideoSessionResponse(
            sessionId=request.session_id,
            token=connection["token"],
            openviduUrl=settings.OPENVIDU_URL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recording/start")
def start_recording(
    session_id: str,
    user=Depends(verify_token)
):
    try:
        recording = OpenViduService.start_recording(session_id)
        return {"recordingId": recording["id"], "status": recording["status"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recording/stop")
def stop_recording(
    recording_id: str,
    user=Depends(verify_token)
):
    try:
        recording = OpenViduService.stop_recording(recording_id)
        return {
            "recordingId": recording["id"],
            "status": recording["status"],
            "url": recording.get("url", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recording/{recording_id}")
def get_recording(
    recording_id: str,
    user=Depends(verify_token)
):
    try:
        recording = OpenViduService.get_recording(recording_id)
        return {
            "recordingId": recording["id"],
            "status": recording["status"],
            "url": recording.get("url", "")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/recording/{recording_id}/download")
def download_recording(
    recording_id: str,
    user=Depends(verify_token)
):
    url = f"{settings.OPENVIDU_URL}/openvidu/recordings/{recording_id}/{recording_id}.mp4"
    try:
        response = httpx.get(
            url,
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False,
            follow_redirects=True
        )
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Recording not found")
        from fastapi.responses import Response
        return Response(
            content=response.content,
            media_type="video/mp4",
            headers={
                "Content-Disposition": f"attachment; filename=recording_{recording_id}.mp4"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))