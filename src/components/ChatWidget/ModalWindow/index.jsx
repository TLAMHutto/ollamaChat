import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { styles } from "./../styles";

function ModalWindow(props) {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const chatResponseRef = useRef(null);

    const handleQuery = async () => {
        try {
            const result = await axios.post('http://localhost:3001/query', { message });
            setMessages((prevMessages) => [...prevMessages, result.data.response]);
            setMessage('');
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

    useEffect(() => {
        if (chatResponseRef.current) {
            chatResponseRef.current.scrollTop = chatResponseRef.current.scrollHeight;
        }
    }, [messages]);

    return (
        <div
            style={{
                ...styles.modalWindow,
                opacity: props.visible ? "1" : "0",
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
            }}
        >
            <div 
                className='chat-response' 
                ref={chatResponseRef}
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
                    <p key={index} style={{margin: '10px 0'}}>{msg}</p>
                ))}
            </div>
            <div style={{ display: 'flex', marginTop: 'auto' }}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message here..."
                    style={{ 
                        flex: 1, 
                        marginRight: '10px', 
                        padding: '10px',
                        borderRadius: '5px',
                        border: '1px solid #ccc',
                    }}
                />
                <button 
                    onClick={handleQuery}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                    }}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default ModalWindow;