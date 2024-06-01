import React, { useState } from 'react';
import axios from 'axios';
import Form from './Form';
import Results from './Results';
import './App.css'; // Import your CSS file for custom styling

const App = () => {
  const backendEndpoint = 'http://localhost:5000/api/closest_stations'; // Update to your backend endpoint
  const [stations, setStations] = useState([]);
  const [submittedAddress, setSubmittedAddress] = useState('');

  const handleSubmit = async (address) => {
    try {
      const response = await axios.get(`${backendEndpoint}?address=${address}`);
      setStations(response.data); // Assuming response.data contains the array of police stations
      setSubmittedAddress(address);
    } catch (error) {
      console.error('Error fetching data:', error);
      setStations([]);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">Police Station Finder</h1>
      </header>
      <div className="form-container">
        <Form onSubmit={handleSubmit} />
      </div>
      <div className="results-container">
        <Results address={submittedAddress} stations={stations} />
      </div>
    </div>
  );
};

export default App;
