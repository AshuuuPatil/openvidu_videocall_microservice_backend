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

    @staticmethod
    def start_recording(session_id: str):
        url = f"{settings.OPENVIDU_URL}/openvidu/api/recordings/start"
        payload = {
            "session": session_id,
            "outputMode": "COMPOSED",
            "hasAudio": True,
            "hasVideo": True,
            "recordingLayout": "BEST_FIT"
        }
        response = requests.post(
            url,
            json=payload,
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False
        )
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to start recording: {response.text}")
        return response.json()

    @staticmethod
    def stop_recording(recording_id: str):
        url = f"{settings.OPENVIDU_URL}/openvidu/api/recordings/stop/{recording_id}"
        response = requests.post(
            url,
            json={},
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False
        )
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to stop recording: {response.text}")
        return response.json()

    @staticmethod
    def get_recording(recording_id: str):
        url = f"{settings.OPENVIDU_URL}/openvidu/api/recordings/{recording_id}"
        response = requests.get(
            url,
            auth=(settings.OPENVIDU_USERNAME, settings.OPENVIDU_SECRET),
            verify=False
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get recording: {response.text}")
        return response.json()