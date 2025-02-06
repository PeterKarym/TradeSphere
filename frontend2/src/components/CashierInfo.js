import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CashierInfo = () => {
    const [cashierInfo, setCashierInfo] = useState(null);

    useEffect(() => {
        const fetchCashierInfo = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/cashier-info/');
                setCashierInfo(response.data);
            } catch (error) {
                console.error('Error fetching cashier information:', error);
            }
        };

        fetchCashierInfo();
    }, []);

    return (
        <div>
            <h2>Cashier Information</h2>
            {cashierInfo ? (
                <div>
                    <p>Cashier Name: {cashierInfo.cashier_name}</p>
                    <p>Supported Currencies: {cashierInfo.supported_currencies ? cashierInfo.supported_currencies.join(', ') : 'No supported currencies available'}</p>
                </div>
            ) : (
                <p>Loading cashier information...</p>
            )}
        </div>
    );
};

export default CashierInfo;
