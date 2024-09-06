import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import ollama from 'ollama'
const SettingsCard = () => {
  const [aiModel, setAiModel] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [models, setModels] = useState([]);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  useEffect(() => {
    async function fetchModels() {
      try {
        const response = await ollama.list();
        console.log(response); // Checking the response structure
        setModels(response.models || []); // Extract models array from the response
      } catch (error) {
        console.error('Error listing models:', error);
      }
    }

    fetchModels();
  }, []);

  const handleAiModelChange = (event) => {
    setAiModel(event.target.value);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
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
