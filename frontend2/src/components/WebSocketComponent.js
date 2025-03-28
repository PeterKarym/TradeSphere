import { useEffect } from 'react';

const WebSocketComponent = ({ onMessage }) => {
  useEffect(() => {
    let socket; // Variable to hold the WebSocket instance
    let retryCount = 0; // Counter for connection retries
    const maxRetries = 5; // Maximum retries allowed

    // Function to establish a WebSocket connection
    const connect = () => {
      socket = new WebSocket('ws://localhost:8080/ws/trading/');

      socket.onopen = () => {
        console.log('WebSocket connection established');
      };

      socket.onmessage = (event) => {
        try {
          const rawMessage = JSON.parse(event.data); // Parse the initial message
          console.log('Received WebSocket message:', rawMessage);

          // Check if the message key contains a string
          if (rawMessage && rawMessage.message) {
            // Parse the comma-separated message string
            const [symbol, signalType, price, timestamp] = rawMessage.message.split(', ');

            // Construct the signal object
            const parsedSignal = {
              symbol: symbol.trim(),
              signalType: signalType.trim(),
              price: parseFloat(price.trim()), // Convert price to a number
              timestamp: timestamp.trim(),
            };

            console.log('Parsed signal:', parsedSignal);

            // Call the onMessage callback with the parsed signal
            if (onMessage) {
              onMessage(parsedSignal);
            }
          } else {
            console.warn('Unexpected WebSocket message format:', rawMessage);
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      socket.onclose = () => {
        console.log('WebSocket connection closed');
        // Retry connection if needed
        if (retryCount < maxRetries) {
          retryCount++;
          console.log(`Retrying connection... (Attempt ${retryCount})`);
          setTimeout(connect, 1000);
        }
      };

      socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    // Establish the WebSocket connection
    connect();

    // Cleanup function when the component unmounts
    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [onMessage]); // Run this effect only once (or when onMessage changes)

  // This component doesn’t need to render any DOM.
  return null;
};

export default WebSocketComponent;
