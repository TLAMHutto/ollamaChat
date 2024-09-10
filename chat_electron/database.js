import { MongoClient } from 'mongodb';

export async function testConnection() {
  const uri = 'mongodb://localhost:27017'; // Replace with your MongoDB connection string
  const client = new MongoClient(uri);

  try {
    await client.connect();
    console.log('Connected successfully to MongoDB');

    // Optionally, list databases
    const dbList = await client.db().admin().listDatabases();
    console.log('Databases:', dbList);

    return dbList; // Return the database list or any other relevant data

  } catch (err) {
    console.error('Error connecting to MongoDB:', err);
    throw err; // Re-throw the error so it can be caught in the component

  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
    console.log('MongoDB connection closed');
  }
}