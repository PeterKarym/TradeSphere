import React, { useState } from 'react';
import axios from 'axios';

const Withdrawal = () => {
    const [email, setEmail] = useState('');
    const [amount, setAmount] = useState('');
    const [message, setMessage] = useState('');

    const handleWithdrawal = async () => {
        try {
            const response = await axios.post('http://localhost:8000/api/withdrawal/', { email, amount });
            setMessage(`Withdrawal initiated! ${response.data.message}`);
        } catch (error) {
            console.error('Error making withdrawal:', error);
            setMessage('Failed to make withdrawal.');
        }
    };

    return (
        <div>
            <h3>Withdrawal</h3>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
            />
            <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="Enter amount"
            />
            <button onClick={handleWithdrawal}>Withdraw</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Withdrawal;
