import React from 'react';
import SettingsCard from '../components/SettingsCard';
import { Box } from '@mui/material';

function Settings({ onAiModelChange }) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',

      }}
    >
      <SettingsCard onAiModelChange={onAiModelChange} />
      {/* Add other settings components here if needed */}
    </Box>
  );
}

export default Settings;
