from datetime import datetime, timedelta
import jwt
from app.config import settings

USERS_DB = {
    "doctor": {"username": "doctor", "password": "123456", "role": "admin"},
    "user": {"username": "user", "password": "123456", "role": "user"},
}

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str):
        user = USERS_DB.get(username)
        if user and user["password"] == password:
            return {"username": username, "role": user["role"]}
        return None

    @staticmethod
    def create_access_token(data: dict, expires_minutes: int = 60):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt