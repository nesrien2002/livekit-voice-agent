"""
Token Server for LiveKit Voice Agent
Provides authentication tokens for frontend clients
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from livekit import api
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


@app.route('/get-token', methods=['GET'])
def get_token():
    """
    Generate LiveKit access token for a user

    Query params:
        room: Room name
        username: User's display name
    """
    room_name = request.args.get('room', 'voice-agent-room')
    username = request.args.get('username', 'guest')

    try:
        # Create access token
        token = api.AccessToken(
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET")
        )

        # Set user identity and permissions
        token.with_identity(username)
        token.with_name(username)
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
            )
        )

        # Generate JWT
        jwt_token = token.to_jwt()

        return jsonify({
            'token': jwt_token,
            'url': os.getenv('LIVEKIT_URL')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("🚀 Starting Token Server...")
    print(f"📡 LiveKit URL: {os.getenv('LIVEKIT_URL')}")
    print(f"🔑 API Key: {os.getenv('LIVEKIT_API_KEY')[:10]}...")
    print("✅ Server running on http://localhost:8000")

    app.run(host='0.0.0.0', port=8000, debug=True)