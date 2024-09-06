import React, { useEffect, useState } from 'react';
import ollama from 'ollama';
import { ThemeProvider, Box, Card, CardContent, Typography, FormControl, InputLabel, Select, MenuItem, createTheme } from '@mui/material';
function SettingsCard({ onAiModelChange }) {
  const [aiModel, setAiModel] = useState('');
  const [models, setModels] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

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

  const handleAiModelChange = (event) => {
    const selectedModel = event.target.value;
    setAiModel(selectedModel);
    if (typeof onAiModelChange === 'function') {
      onAiModelChange(selectedModel);
    } else {
      console.error('onAiModelChange is not a function');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '50%',
          width: '70%'
        }}
      >
        <Card sx={{ width: '100%', maxWidth: 400, m: 2 }}>
          <CardContent>
            <Typography variant="h5" component="div" gutterBottom>
              Settings
            </Typography>

            <Box sx={{ mb: 2 }}>
              <FormControl fullWidth>
                <InputLabel id="ai-model-label">AI Model</InputLabel>
                <Select
                  labelId="ai-model-label"
                  value={aiModel}
                  label="AI Model"
                  onChange={handleAiModelChange}
                >
                  {models.length > 0 ? (
                    models.map((model) => (
                      <MenuItem key={model.name} value={model.name}>
                        {model.name}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem disabled>No models available</MenuItem>
                  )}
                </Select>
              </FormControl>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </ThemeProvider>
  );
};

export default SettingsCard;