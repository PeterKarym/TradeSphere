import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Deposit = () => {
    const [cashierURL, setCashierURL] = useState(null);

    useEffect(() => {
        // Fetch the cashier URL from the server
        axios.get('http://localhost:8000/api/getCashierURL')
            .then(response => {
                if (response.data.cashierURL) {
                    setCashierURL(response.data.cashierURL);
                }
            })
            .catch(error => {
                console.error('Error fetching cashier URL:', error);
            });

        // Set an interval to keep the session alive
        const interval = setInterval(() => {
            axios.get('http://localhost:8000/api/getCashierURL')
                .then(response => {
                    console.log('Session keep-alive response:', response.data);
                })
                .catch(error => {
                    console.error('Error keeping session alive:', error);
                });
        }, 600000); // Every 10 minutes (600000 ms)

        return () => clearInterval(interval); // Cleanup the interval on component unmount
    }, []);

    const openCashier = () => {
        if (window.confirm("Do you want to proceed to the Cashier?")) {
            window.open(cashierURL, "_blank");
        }
    };

    return (
        <div>
            <h3>Deposit</h3>
            {cashierURL ? (
                <div>
                    <p>Please click Open Cashier button below to make a deposit.</p>
                    <button onClick={openCashier}>Open Cashier</button>
                </div>
            ) : (
                <p>Loading Cashier...</p>
            )}
        </div>
    );
};

export default Deposit;
