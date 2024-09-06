import express from 'express';
import cors from 'cors';
import ollama from 'ollama';

const app = express();
const port = 3002;

// Use CORS middleware
app.use(cors());
app.use(express.json());

// Add a route handler for /query
app.post('/query', async (req, res) => {
  try {
    const { message, model } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    if (!model) {
      return res.status(400).json({ error: 'Model is required' });
    }

    // Use ollama to generate a response
    const response = await ollama.chat({
      model: model,
      messages: [{ role: 'user', content: message }],
    });

    res.json({ response: response.message.content });
  } catch (error) {
    console.error('Error processing query:', error);
    res.status(500).json({ error: 'An error occurred while processing your request' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});