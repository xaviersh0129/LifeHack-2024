import React, { useState } from 'react';

const Form = ({ onSubmit }) => {
  const [address, setAddress] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (address.trim()) {
      onSubmit(address);
      setAddress(''); // Clear the input field after submission
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="address">Enter Address:</label>
      <input
        id="address"
        type="text"
        placeholder="Enter address"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
};

export default Form;
