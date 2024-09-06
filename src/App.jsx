// ./renderer/src/App.js (React component)
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import './index.css'
import ChatWidget from './components/ChatWidget'
import { SpeedDialButton } from './components/SpeedDialButton';
import Settings from './pages/Settings'
import HomePage from './pages/HomePage';
function App() {


  return (
    <Router>
      <div>
        <SpeedDialButton />
        <ChatWidget />
        <Routes>
          <Route path="/" element={<HomePage/>}></Route>
          <Route path="/pages/Settings" element={<Settings/>} /> {/* Add your new route here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
