import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './index.css'
import ChatWidget from './components/ChatWidget'
import { SpeedDialButton } from './components/SpeedDialButton';
import Settings from './pages/Settings'
import HomePage from './pages/HomePage';

function App() {
  const [selectedAiModel, setSelectedAiModel] = useState('');

  const handleAiModelChange = (model) => {
    setSelectedAiModel(model);
  };

  return (
    <Router>
      <div>
        <SpeedDialButton />
        <ChatWidget selectedAiModel={selectedAiModel} />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route 
            path="/pages/Settings" 
            element={<Settings onAiModelChange={handleAiModelChange} />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;