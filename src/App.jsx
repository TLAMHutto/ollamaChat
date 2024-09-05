// ./renderer/src/App.js (React component)
import React, { useState } from 'react';
import axios from 'axios';
import ChatWidget from './components/ChatWidget'
import { SpeedDialButton } from './components/SpeedDialButton';
import './index.css'
function App() {


  return (
    <div>
      <SpeedDialButton />
      <ChatWidget />
    </div>
  );
}

export default App;
