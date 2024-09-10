import React, { useEffect, useState } from 'react';
import { testConnection } from '../../database.js';
import DatabaseInfoDisplay from './DatabaseInfoDisplay';
import { ButtonGroup, Button } from '@mui/material';
import './styles/Database.css'
const Database = () => {
  const [dbInfo, setDbInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await testConnection();
        setDbInfo(result);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-8 text-center">Local Storage</h2>
      {error ? (
        <p className="text-red-500">Error: {error}</p>
      ) : dbInfo ? (
        <DatabaseInfoDisplay dbInfo={dbInfo} />
      ) : (
        <p>Loading...</p>
      )}
      <ButtonGroup variant="text" aria-label="Basic button group" className="button-group-container">
        <Button>Create Database</Button>
        <Button>Add to database</Button>
        <Button>Delete Database</Button>
      </ButtonGroup>
    </div>
  );
};

export default Database;