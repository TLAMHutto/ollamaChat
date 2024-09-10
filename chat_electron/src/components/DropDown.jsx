import { Select } from 'antd';
import React, { useState, useEffect } from 'react';
import ollama from 'ollama';

const DropDown = ({ onAiModelChange }) => {
  const [aiModel, setAiModel] = useState('');
  const [models, setModels] = useState([]);

  useEffect(() => {
    async function fetchModels() {
      try {
        const response = await ollama.list();
        setModels(response.models || []);
      } catch (error) {
        console.error('Error listing models:', error);
      }
    }

    fetchModels();
  }, []);

  const handleAiModelChange = (value) => {
    setAiModel(value);
    if (typeof onAiModelChange === 'function') {
      onAiModelChange(value);
    } else {
      console.error('onAiModelChange is not a function');
    }
  };

  return (
    <Select
      style={{ width: 200 }}
      value={aiModel}
      onChange={handleAiModelChange}
      placeholder="Select AI Model"
    >
      {models.length > 0 ? (
        models.map((model) => (
          <Select.Option key={model.name} value={model.name}>
            {model.name}
          </Select.Option>
        ))
      ) : (
        <Select.Option disabled>No models available</Select.Option>
      )}
    </Select>
  );
};

export default DropDown;
