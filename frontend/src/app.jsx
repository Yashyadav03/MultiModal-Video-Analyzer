import { useState } from 'react';
import VideoInput from './components/VideoInput';
import Transcript from './components/Transcript';
import Chat from './components/Chat';

function App() {
  const [videoId, setVideoId] = useState(null);
  const [transcript, setTranscript] = useState('');

  const handleVideoProcessed = (id, text) => {
    setVideoId(id);
    setTranscript(text);
  };

  return (
    <div className="app">
      <header>
        <h1>YouTube Video Analyzer</h1>
        <p>Analyze YouTube videos and ask questions about their content</p>
      </header>

      <main>
        <VideoInput onVideoProcessed={handleVideoProcessed} />
        
        {transcript && (
          <>
            <Transcript text={transcript} />
            <Chat videoId={videoId} />
          </>
        )}
      </main>
    </div>
  );
}

export default App;