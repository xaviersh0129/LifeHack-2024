import React from 'react';

const Results = ({ stations }) => {
  if (!stations.length) {
    return <div>No results found.</div>;
  }

  return (
    <div>
      <h2>Top 3 Closest Police Stations</h2>
      <ul>
        {stations.map((station, index) => (
          <li key={index}>
            {station.name} - {station.address} ({station.travelTime.toFixed(2)} minutes)
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Results;