import React, { useState } from 'react';
import axios from 'axios';
import Form from './Form';
import Results from './Results';

const App = () => {
  const backendEndpoint = 'http://localhost:5000/api/closest_stations'; // Update to your backend endpoint
  const [stations, setStations] = useState([]);

  const handleSubmit = async (address) => {
    try {
      const response = await axios.get(`${backendEndpoint}?address=${address}`);
      setStations(response.data); // Assuming response.data contains the array of police stations
    } catch (error) {
      console.error('Error fetching data:', error);
      setStations([]);
    }
  };

  return (
    <div>
      <h1>Police Station Finder</h1>
      <Form onSubmit={handleSubmit} />
      <Results stations={stations} />
    </div>
  );
};

export default App;