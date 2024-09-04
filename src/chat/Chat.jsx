// ./renderer/src/Chat.js
import React, { useState } from 'react';
import axios from 'axios';
import './chat.css'; // Make sure to import your CSS file

function Chat() {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]); // Array to store messages

  const handleQuery = async () => {
    try {
      const result = await axios.post('http://localhost:3001/query', { message });
      setMessages((prevMessages) => [...prevMessages, result.data.response]); // Add new message to the list
      setMessage(''); // Clear input field
    } catch (error) {
      console.error('Error querying the API:', error);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleQuery();
    }
  };

  return (
    <div className='chat-container'>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button onClick={handleQuery}>Send</button>
      <div className='chat-response'>
        {messages.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
    </div>
  );
}

export default Chat;
