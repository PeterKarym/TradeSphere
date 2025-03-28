import React, { useState } from 'react';
import WebSocketComponent from '../components/WebSocketComponent'; // Adjust path as necessary

const MT5Report = () => {
  const [signal, setSignal] = useState(null); // State to hold the received signal

  // Callback function to update state when WebSocketComponent receives a message
  const handleNewMessage = (message) => {
    console.log('Received signal in MT5Report:', message); // Log the received signal
    setSignal(message); // Update the state
  };

  return (
    <div>
      <h3>MT5 Report</h3>
      {/* Include the WebSocketComponent and pass the callback */}
      <WebSocketComponent onMessage={handleNewMessage} />

      {signal ? (
        <div>
          <p><strong>Symbol:</strong> {signal.symbol}</p>
          <p><strong>Signal Type:</strong> {signal.signalType}</p>
          <p><strong>Price:</strong> {signal.price}</p>
          <p><strong>Timestamp:</strong> {signal.timestamp}</p>
        </div>
      ) : (
        <p>No signal received yet.</p>
      )}
    </div>
  );
};

export default MT5Report;
