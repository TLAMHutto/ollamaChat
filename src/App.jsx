// ./renderer/src/App.js (React component)
import React, { useState } from 'react';
import axios from 'axios';
import ChatWidget from './components/ChatWidget'


function App() {


  return (
    <div>
      <ChatWidget />
    </div>
  );
}

export default App;
