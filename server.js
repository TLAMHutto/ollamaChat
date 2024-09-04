// ./src/server.js (Express server)
import express from 'express';
import cors from 'cors'; // Import the cors package
import ollama from 'ollama';

const app = express();
const port = 3001;

// Use CORS middleware
app.use(cors());
app.use(express.json());

app.post('/query', async (req, res) => {
  try {
    const response = await ollama.chat({
      model: 'llama3.1',
      messages: [{ role: 'user', content: req.body.message }],
    });
    res.json({ response: response.message.content });
  } catch (error) {
    console.error('Error with Ollama API:', error);
    res.status(500).json({ error: 'Error with Ollama API' });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
