
// src/components/AccountBalances.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/AccountBalances.css'; // Adjusted the path

const AccountBalances = () => {
    const [balances, setBalances] = useState({ 
        demo_accounts: {},
        real_accounts: {},
        total_demo_assets_balance: 0,
        total_real_assets_balance: 0 
    });

    useEffect(() => {
        const fetchBalances = async () => {
            try {
                // Update the API URL to the correct Django server port
                const response = await axios.get('http://localhost:8000/api/account-balances/');
                setBalances(response.data);
            } catch (error) {
                console.error('Error fetching account balances:', error);
            }
        };

        fetchBalances();

        // Optional: Refresh balances every 60 seconds
        const interval = setInterval(fetchBalances, 60000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="account-balances">
            <h2>Account Balances</h2>
            <h3>Demo Accounts</h3>
            {Object.entries(balances.demo_accounts || {}).map(([account, balance]) => (
                <p key={account}>Account {account}: {balance} USD</p>
            ))}
            <h3>Real Accounts</h3>
            {Object.entries(balances.real_accounts || {}).map(([account, balance]) => (
                <p key={account}>Account {account}: {balance} USD</p>
            ))}
            <h3>Total Assets</h3>
            <p>Total Demo Assets Balance: {balances.total_demo_assets_balance || 0} USD</p>
            <p>Total Real Assets Balance: {balances.total_real_assets_balance || 0} USD</p>
        </div>
    );
};

export default AccountBalances;