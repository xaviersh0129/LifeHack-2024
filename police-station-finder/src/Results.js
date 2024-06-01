import React from 'react';
import './Results.css'; // Import Results specific styles

const Results = ({ address, stations }) => {
  if (!stations.length) {
    return <div className="no-results">No results found.</div>;
  }

  return (
    <div>
      <h2 className="results-title">Top 3 Closest Police Stations</h2>
      <p className="submitted-address">Address submitted: {address}</p>
      <ul className="results-list">
        {stations.map((station, index) => (
          <li key={index} className="result-item">
            <div className="station-name">{station.name}</div>
            <div className="station-address">{station.address}</div>
            <div className="travel-time">{station.travelTime.toFixed(2)} minutes</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Results;
