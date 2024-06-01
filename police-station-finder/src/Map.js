import React from 'react';
import { GoogleMap, LoadScript, DirectionsService, DirectionsRenderer, Marker } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '400px'
};

const center = {
  lat: 1.3521, // Default latitude of Singapore
  lng: 103.8198 // Default longitude of Singapore
};

const Map = ({ origin, destinations, stations }) => {
  const [response, setResponse] = React.useState(null);

  const directionsCallback = (res) => {
    if (res !== null) {
      if (res.status === 'OK') {
        setResponse(res);
      } else {
        console.error(`error fetching directions ${res}`);
      }
    }
  };

  return (
    <LoadScript googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={11}
      >
        {origin && destinations && destinations.length > 0 && (
          <>
            <DirectionsService
              options={{
                origin: origin,
                destination: destinations[0], // You can set to the nearest station
                travelMode: 'DRIVING',
                waypoints: destinations.slice(1).map(dest => ({ location: dest })),
                optimizeWaypoints: true
              }}
              callback={directionsCallback}
            />
            {response !== null && (
              <DirectionsRenderer
                options={{
                  directions: response
                }}
              />
            )}
          </>
        )}
        {stations && stations.map((station, index) => (
          <Marker
            key={index}
            position={{ lat: station.lat, lng: station.lng }}
            label={`${station.crimeValue}`}
            title={`Crime Value: ${station.crimeValue}`}
          />
        ))}
      </GoogleMap>
    </LoadScript>
  );
};

export default Map;
