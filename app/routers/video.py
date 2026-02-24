# from fastapi import APIRouter, Depends, HTTPException
# from app.schemas.video_schema import VideoSessionRequest, VideoSessionResponse
# from app.services.openvidu_service import OpenViduService
# from app.dependencies import verify_token
# from app.config import settings

# router = APIRouter(prefix="/api/video", tags=["Video"])

# @router.post("/session", response_model=VideoSessionResponse)
# def create_video_session(
# request: VideoSessionRequest,
# user=Depends(verify_token)
# ):
#     try:
#         # Create session if not exists
#         OpenViduService.create_session(request.session_id)
            
#         # Create connection token
#         connection = OpenViduService.create_connection(request.session_id)

#         return VideoSessionResponse(
#             sessionId=request.session_id,
#             token=connection["token"],
#             openviduUrl=settings.OPENVIDU_URL
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





import requests
from app.config import settings

class OpenViduService:

    @staticmethod
    def create_session(custom_session_id: str = None):
        url = f"{settings.OPENVIDU_URL}/openvidu/api/sessions"
        payload = {}
        if custom_session_id:
            payload["customSessionId"] = custom_session_id
        response = requests.post(
            url,
            json=payload,
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False
        )
        if response.status_code in [200, 201]:
            return response.json()
        elif response.status_code == 409:
            # Session already exists — this is fine, return session id
            return {"id": custom_session_id}
        else:
            raise Exception(f"Failed to create session: {response.text}")

    @staticmethod
    def create_connection(session_id: str):
        url = f"{settings.OPENVIDU_URL}/openvidu/api/sessions/{session_id}/connection"
        response = requests.post(
            url,
            json={},
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False
        )
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create connection: {response.text}")
        return response.json()