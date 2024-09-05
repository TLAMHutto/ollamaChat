// ./renderer/src/App.js (React component)
import React, { useState } from 'react';
import axios from 'axios';
import ChatWidget from './components/ChatWidget'


function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleQuery = async () => {
    try {
      const result = await axios.post('http://localhost:3001/query', { message });
      setResponse(result.data.response);
    } catch (error) {
      console.error('Error querying the API:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={handleQuery}>Send</button>
      <pre>{response}</pre>
      <ChatWidget />
    </div>
  );
}

export default App;
