import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  Button,
  Box,
  ThemeProvider,
  createTheme,
} from '@mui/material';

const SettingsCard = () => {
  const [aiModel, setAiModel] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [selectedDirectory, setSelectedDirectory] = useState('');

  const handleAiModelChange = (event) => {
    setAiModel(event.target.value);
  };

  const handleThemeChange = () => {
    setDarkMode(!darkMode);
  };

  const handleDirectorySelection = () => {
    // Implement directory selection logic here
    // For now, we'll just set a placeholder value
    setSelectedDirectory('/user/documents/app-data');
  };

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <Box 
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh', // This ensures the box takes up the full viewport height
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
                  <MenuItem value="gpt-3.5">GPT-3.5</MenuItem>
                  <MenuItem value="gpt-4">GPT-4</MenuItem>
                  <MenuItem value="claude-2">Claude 2</MenuItem>
                </Select>
              </FormControl>
            </Box>

            <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Typography>Dark Mode</Typography>
              <Switch
                checked={darkMode}
                onChange={handleThemeChange}
                inputProps={{ 'aria-label': 'theme switch' }}
              />
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography gutterBottom>Selected Directory:</Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                {selectedDirectory || 'No directory selected'}
              </Typography>
              <Button variant="outlined" onClick={handleDirectorySelection}>
                Select Directory
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Box>
    </ThemeProvider>
  );
};

export default SettingsCard;