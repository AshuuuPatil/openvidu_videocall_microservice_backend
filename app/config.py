from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENVIDU_URL = os.getenv("OPENVIDU_URL")
    OPENVIDU_USERNAME = os.getenv("OPENVIDU_USERNAME")
    OPENVIDU_SECRET = os.getenv("OPENVIDU_SECRET")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()