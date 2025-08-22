import { useState } from 'react';
import axios from 'axios';

const Chat = ({ videoId }) => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const askQuestion = async () => {
    if (!question) return;

    setLoading(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/chat/ask', {
        video_id: videoId,
        question: question
      });

      const newQa = {
        question,
        answer: response.data.answer,
        sources: response.data.sources
      };

      setHistory([...history, newQa]);
      setAnswer(response.data.answer);
      setQuestion('');
    } catch (err) {
      console.error('Error asking question:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat">
      <h2>Ask Questions About the Video</h2>
      
      <div className="chat-input">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about the video..."
          disabled={loading}
          onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
        />
        <button onClick={askQuestion} disabled={loading}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

      <div className="chat-history">
        {history.map((item, index) => (
          <div key={index} className="qa-pair">
            <div className="question"><strong>Q:</strong> {item.question}</div>
            <div className="answer"><strong>A:</strong> {item.answer}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chat;