import React, { useState } from 'react';
import ModalWindow from './ChatWidget/ModalWindow';
import SettingsCard from './SettingsCard';

const ParentComponent = () => {
  const [aiModel, setAiModel] = useState('');  // Define aiModel and setAiModel here
  const [isModalVisible, setIsModalVisible] = useState(true);  // Control modal visibility

  return (
    <div>
      {/* Ensure you are passing setAiModel and aiModel correctly */}
      <SettingsCard setAiModel={setAiModel} aiModel={aiModel} />

      {/* Toggle modal visibility */}
      <button onClick={() => setIsModalVisible(!isModalVisible)}>
        Toggle Modal
      </button>

      {/* Pass aiModel and modal visibility to ModalWindow */}
      <ModalWindow aiModel={aiModel} visible={isModalVisible} />
    </div>
  );
};

export default ParentComponent;
