import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AccountBalances from '../components/AccountBalances';
import CashierInfo from '../components/CashierInfo'; // Importing CashierInfo component

const Dashboard = () => {
  const [cashierURL, setCashierURL] = useState(null);

  // Function to fetch cashier URL from the server
  useEffect(() => {
    axios.get('http://localhost:8000/api/getCashierURL') // Updated URL with correct base
      .then(response => {
        if (response.data.cashierURL) {
          console.log('Cashier URL:', response.data.cashierURL); // Debugging log
          setCashierURL(response.data.cashierURL);
        } else {
          console.log('Cashier URL not found in response:', response.data); // Debugging log
        }
      })
      .catch(error => {
        console.error('Error fetching cashier URL:', error);
      });
  }, []);
   /* Prompt the user to confirm the action before redirecting them to the URL.SECURITY MEASURE */
  const openCashier = () => {
    if (window.confirm("Do you want to proceed to the Cashier?")) {
      window.open(cashierURL, "_blank");
    }
  };

  return (
    <div>
      <h2>Welcome to the Dashboard</h2>
      <AccountBalances /> {/* Adding AccountBalances component */}
      <CashierInfo /> {/* Adding CashierInfo component */}
      {/* Button to open Cashier */}
      {cashierURL && (
        <button onClick={openCashier}>
          Open Cashier
        </button>
      )}
      {/* Other dashboard components can go here */}
    </div>
  );
};

export default Dashboard;
