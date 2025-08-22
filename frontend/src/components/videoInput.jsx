import { useState } from 'react';
import axios from 'axios';

const VideoInput = ({ onVideoProcessed }) => {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const processVideo = async () => {
    if (!youtubeUrl) {
      setError('Please enter a YouTube URL');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/video/process', {
        youtube_url: youtubeUrl
      });

      onVideoProcessed(response.data.video_id, response.data.transcript);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing video');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="video-input">
      <h2>Enter YouTube Video URL</h2>
      <div className="input-group">
        <input
          type="text"
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          disabled={loading}
        />
        <button onClick={processVideo} disabled={loading}>
          {loading ? 'Processing...' : 'Process Video'}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default VideoInput;