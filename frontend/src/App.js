import React, { useState, useEffect, useRef } from 'react';
import { Room, RoomEvent } from 'livekit-client';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const LIVEKIT_URL = process.env.REACT_APP_LIVEKIT_URL || 'wss://voice-agent-k9vtl1in.livekit.cloud';

function App() {
  const [userName, setUserName] = useState('');
  const [roomName, setRoomName] = useState('voice-agent-room');
  const [connected, setConnected] = useState(false);
  const [status, setStatus] = useState('Disconnected');
  const [transcripts, setTranscripts] = useState([]);
  const roomRef = useRef(null);
  const audioElementRef = useRef(null);

  const getToken = async () => {
    try {
      const response = await fetch(
        `${BACKEND_URL}/get-token?room=${roomName}&username=${userName}`
      );
      const data = await response.json();
      return data.token;
    } catch (error) {
      console.error('Error getting token:', error);
      alert('Could not connect to token server. Make sure it is running on port 8000.');
      return null;
    }
  };

  const handleConnect = async () => {
    if (!userName.trim()) {
      alert('Please enter your name');
      return;
    }

    setStatus('Connecting...');

    try {
      const token = await getToken();
      if (!token) {
        setStatus('Failed to get token');
        return;
      }

      const room = new Room({
        adaptiveStream: true,
        dynacast: true,
      });

      roomRef.current = room;

      room.on(RoomEvent.Connected, () => {
        console.log('Connected to room');
        setConnected(true);
        setStatus('Connected - Speak to the agent');
        addTranscript('system', 'Connected! The agent is listening...');
      });

      room.on(RoomEvent.Disconnected, () => {
        console.log('Disconnected from room');
        setConnected(false);
        setStatus('Disconnected');
        addTranscript('system', 'Disconnected from voice agent');
      });

      room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
        console.log('Track subscribed:', track.kind);
        
        if (track.kind === 'audio') {
          const audioElement = track.attach();
          audioElementRef.current = audioElement;
          document.body.appendChild(audioElement);
          audioElement.play();
          addTranscript('agent', 'Agent audio track connected');
        }
      });

      room.on(RoomEvent.TrackUnsubscribed, (track) => {
        console.log('Track unsubscribed:', track.kind);
        track.detach();
      });

      await room.connect(LIVEKIT_URL, token);
      await room.localParticipant.setMicrophoneEnabled(true);
      console.log('Microphone enabled');
      
    } catch (error) {
      console.error('Connection error:', error);
      setStatus('Connection failed: ' + error.message);
      alert('Connection failed. Check console for details.');
    }
  };

  const handleDisconnect = async () => {
    if (roomRef.current) {
      await roomRef.current.disconnect();
      roomRef.current = null;
    }
    
    if (audioElementRef.current) {
      audioElementRef.current.remove();
      audioElementRef.current = null;
    }
    
    setConnected(false);
    setStatus('Disconnected');
    setTranscripts([]);
  };

  const addTranscript = (type, text) => {
    setTranscripts(prev => [...prev, { type, text, timestamp: new Date() }]);
  };

  useEffect(() => {
    return () => {
      if (roomRef.current) {
        roomRef.current.disconnect();
      }
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎤 AI Voice Agent</h1>
        
        {!connected ? (
          <div className="connect-form">
            <div className="status-badge">{status}</div>
            
            <input
              type="text"
              placeholder="Enter your name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="input-field"
              onKeyPress={(e) => e.key === 'Enter' && handleConnect()}
            />
            
            <input
              type="text"
              placeholder="Room name (optional)"
              value={roomName}
              onChange={(e) => setRoomName(e.target.value)}
              className="input-field"
            />
            
            <button onClick={handleConnect} className="connect-button">
              Connect to Voice Agent
            </button>
            
            <div className="info">
              <p>🔹 Make sure your microphone is enabled</p>
              <p>🔹 Token server should be running on port 8000</p>
              <p>🔹 Voice agent should be running</p>
            </div>
          </div>
        ) : (
          <div className="voice-chat">
            <div className="status-badge connected">{status}</div>
            
            <div className="controls">
              <div className="mic-indicator">
                🎤 Microphone Active
              </div>
            </div>
            
            <div className="transcripts">
              <h3>Activity Log:</h3>
              {transcripts.length === 0 ? (
                <p className="hint">Waiting for activity...</p>
              ) : (
                transcripts.map((t, idx) => (
                  <div key={idx} className={`message ${t.type}`}>
                    <strong>
                      {t.type === 'user' ? '👤 You' : 
                       t.type === 'agent' ? '🤖 Agent' : 'ℹ️ System'}:
                    </strong> {t.text}
                  </div>
                ))
              )}
            </div>
            
            <button onClick={handleDisconnect} className="disconnect-button">
              Disconnect
            </button>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
