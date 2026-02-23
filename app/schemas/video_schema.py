from pydantic import BaseModel

class VideoSessionRequest(BaseModel):
    session_id: str

class VideoSessionResponse(BaseModel):
    sessionId: str
    token: str
    openviduUrl: str