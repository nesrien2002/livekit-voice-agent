import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

def test_connection():
    try:
        # Generate a test token
        token = api.AccessToken(
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET")
        )
        token.with_identity("test-user")
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room="test-room",
            )
        )
        jwt = token.to_jwt()
        print("✅ LiveKit connection test successful!")
        print(f"Generated token: {jwt[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()