import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { styles } from '../styles'
import DeleteIcon from '@mui/icons-material/Refresh';
import { IconButton } from '@mui/material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { pojoaque } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './style.css'
function ModalWindow({ visible, selectedAiModel }) {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [error, setError] = useState(null);
    const chatResponseRef = useRef(null);
    const textAreaRef = useRef(null)
    const handleQuery = async () => {
        setError(null); // Clear any previous errors
        try {
            const result = await axios.post('http://localhost:3002/query', { 
                message,
                model: selectedAiModel
            });
            setMessages((prevMessages) => [...prevMessages, { text: message, sender: 'user' }, { text: result.data.response, sender: 'ai' }]);
            setMessage('');
        } catch (error) {
            console.error('Error querying the API:', error);
            if (error.code === 'ERR_NETWORK') {
                setError('Unable to connect to the server. Please check if the server is running and try again.');
            } else {
                setError('An error occurred while processing your request. Please try again.');
            }
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleQuery();
        }
    };
    const handleClear = (e) => {
        e.preventDefault();
        setMessages('');
        setMessages([])
    }
    useEffect(() => {
        if (chatResponseRef.current) {
            chatResponseRef.current.scrollTop = chatResponseRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div className='chat-container' style={{
                ...styles.modalWindow,
                opacity: visible ? "1" : "0",
        }}>
    <div className="chat-messages" ref={chatResponseRef}>
      {messages.map((msg, index) => (
        <pre key={index} className={`message ${msg.sender}`}>
          <SyntaxHighlighter language="javascript" style={pojoaque}
            lineProps={{style: {wordBreak: 'break-all', whiteSpace: 'pre-wrap'}}}
            wrapLines={true}
          >
            {msg.text}
          </SyntaxHighlighter>
        </pre>
      ))}
      {error && <div className="error-message">{error}</div>}
    </div>
            <div className="chat-input" style={{ display: 'flex', marginTop: 'auto' }}>
            <textarea
                    ref={textAreaRef}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                />
                <button onClick={handleQuery}>Send</button>
                <IconButton className='refresh' aria-label="clear" onClick={handleClear}>
                    <DeleteIcon style={{ color: '#afa571' }} /> {/* Change the color here */}
                </IconButton>

            </div>
            <div className="selected-model">
                Selected AI Model: {selectedAiModel || 'None'}
            </div>
        </div>
    );
}

export default ModalWindow;