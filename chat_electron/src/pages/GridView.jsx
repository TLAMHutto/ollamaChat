import React, { useState, useRef, useEffect } from 'react';
import DropDown from '../components/DropDown';
import { Col, Row, Input, Button } from 'antd';
import axios from 'axios';import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { pojoaque } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './styles/Grid.css';

const GridView = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  const [selectedAiModel, setSelectedAiModel] = useState('');
  const [isModalVisible, setModalVisible] = useState(false);
  const chatResponseRef = useRef(null);
  const textAreaRef = useRef(null)

  const handleAiModelChange = (selectedModel) => {
    setSelectedAiModel(selectedModel);
    console.log(selectedModel);
  };

  useEffect(() => {
    if (chatResponseRef.current) {
      chatResponseRef.current.scrollTop = chatResponseRef.current.scrollHeight;
    }
  }, [messages]);
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleQuery();
    }
  };

  const handleQuery = async () => {
    setError(null); // Clear any previous errors

    if (!message.trim()) {
      setError('Please enter a message before sending.');
      return;
    }

    if (!selectedAiModel) {
      setError('Please select an AI model before sending.');
      return;
    }

    try {
      const result = await axios.post('http://localhost:3002/query', {
        message,
        model: selectedAiModel // Use selectedAiModel here
      });
      setMessages((prevMessages) => [...prevMessages, { text: message, sender: 'user' }, { text: result.data.response, sender: 'ai' }]);
      setMessage('');
    } catch (error) {
      console.error('Error querying the API:', error);
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setError(`Server error: ${error.response.status} - ${error.response.data.message || 'Unknown error'}`);
      } else if (error.request) {
        // The request was made but no response was received
        setError('No response received from the server. Please check if the server is running.');
      } else {
        // Something happened in setting up the request that triggered an Error
        setError(`Error: ${error.message}`);
      }
    }
  };



  return (
    <>
      <Row align="middle" className="input-button-row">
        <Col span={18}>
        <textarea
        ref={textAreaRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        style={{
          width: '100%',
          padding: '8px 11px',
          borderRadius: '6px',
          border: '1px solid #d9d9d9',
          resize: 'vertical',
          minHeight: '32px',
          fontFamily: 'inherit',
          fontSize: 'inherit',
        }}
      />
        </Col>
        <Col span={6}>
          <Button type="primary" style={{ width: '100%' }} onClick={handleQuery}>
            Send
          </Button>
        </Col>
      </Row>
      <Row gutter={[16, 16]}>

        <Col span={12}>
          <Row>
            <Col span={24}><DropDown onAiModelChange={handleAiModelChange} />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <div className="chat-messages" ref={chatResponseRef}>
                {messages.map((msg, index) => (
                  <pre key={index} className={`message ${msg.sender}`}>
                    <SyntaxHighlighter language="javascript" style={pojoaque}
                      lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
                      wrapLines={true}
                    >
                      {msg.text}
                    </SyntaxHighlighter>
                  </pre>
                ))}
                {error && <div className="error-message">{error}</div>}
              </div>
            </Col>
          </Row>
        </Col>

        <Col span={12}>
          <Row>
            <Col span={24}><DropDown onAiModelChange={handleAiModelChange} />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <div className="chat-messages" ref={chatResponseRef}>
                {messages.map((msg, index) => (
                  <pre key={index} className={`message ${msg.sender}`}>
                    <SyntaxHighlighter language="javascript" style={pojoaque}
                      lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
                      wrapLines={true}
                    >
                      {msg.text}
                    </SyntaxHighlighter>
                  </pre>
                ))}
                {error && <div className="error-message">{error}</div>}
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
      <Row gutter={[16, 16]}>

      <Col span={12}>
          <Row>
            <Col span={24}><DropDown onAiModelChange={handleAiModelChange} />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <div className="chat-messages" ref={chatResponseRef}>
                {messages.map((msg, index) => (
                  <pre key={index} className={`message ${msg.sender}`}>
                    <SyntaxHighlighter language="javascript" style={pojoaque}
                      lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
                      wrapLines={true}
                    >
                      {msg.text}
                    </SyntaxHighlighter>
                  </pre>
                ))}
                {error && <div className="error-message">{error}</div>}
              </div>
            </Col>
          </Row>
        </Col>
        <Col span={12}>
          <Row>
            <Col span={24}><DropDown onAiModelChange={handleAiModelChange} />
            </Col>
          </Row>
          <Row>
            <Col span={24}>
              <div className="chat-messages" ref={chatResponseRef}>
                {messages.map((msg, index) => (
                  <pre key={index} className={`message ${msg.sender}`}>
                    <SyntaxHighlighter language="javascript" style={pojoaque}
                      lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
                      wrapLines={true}
                    >
                      {msg.text}
                    </SyntaxHighlighter>
                  </pre>
                ))}
                {error && <div className="error-message">{error}</div>}
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
    </>
  );
};

export default GridView;