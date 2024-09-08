import React, { useState, useEffect } from 'react';
import ollama from 'ollama';
import './styles/HomePage.css'
function HomePage() {
  const [modelCount, setModelCount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchModelCount() {
      try {
        const response = await ollama.list();
        console.log('Response:', response); // Log the response to inspect its format

        if (response.models && Array.isArray(response.models)) {
          setModelCount(response.models.length);
        } else {
          throw new Error('Unexpected response format');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchModelCount();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {modelCount !== null ? (
        <p className='models-loaded'>Ollama running with {modelCount} models loaded</p>
      ) : (
        <p>No models found</p>
      )}
    </div>
  );
}

export default HomePage;
