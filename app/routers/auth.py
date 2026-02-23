from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = AuthService.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthService.create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return LoginResponse(access_token=access_token, role=user["role"])