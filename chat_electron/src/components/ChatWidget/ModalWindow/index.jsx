import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { styles } from "./../styles";
import DeleteIcon from '@mui/icons-material/Refresh';
import { IconButton } from '@mui/material';
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
        <div style={{
                ...styles.modalWindow,
                opacity: visible ? "1" : "0",
                display: 'flex',
                flexDirection: 'column',
                height: '80vh',
                width: '80vw',
                maxWidth: '600px',
                margin: 'auto',
                padding: '20px',
                boxSizing: 'border-box',
                backgroundColor: '#f0f1f0',
                borderRadius: '10px',
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                zIndex: 10,
        }}>
            <div className="chat-messages" ref={chatResponseRef}
            style={{
                flex: 1,
                overflowY: 'auto',
                marginBottom: '20px',
                padding: '10px',
                backgroundColor: 'white',
                borderRadius: '5px',
                zIndex: 100,
                position: 'relative',
            }}
            >
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
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
                    style={{ 
                        flex: 1, 
                        marginRight: '10px', 
                        padding: '10px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                        maxHeight: '150px', // Set your desired maximum height
                        overflowY: 'auto', // Enable vertical scroll if content exceeds max height
                        resize: 'none', // Disable manual resize by the user
                    }}
                />
                <button onClick={handleQuery}>Send</button>
                <IconButton aria-label="clear" onClick={handleClear}>
                    <DeleteIcon />
                </IconButton>
            </div>
            <div className="selected-model">
                Selected AI Model: {selectedAiModel || 'None'}
            </div>
        </div>
    );
}

export default ModalWindow;