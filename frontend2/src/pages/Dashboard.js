import React from 'react';
import AccountBalances from '../components/AccountBalances';
import CashierInfo from '../components/CashierInfo';
import Deposit from '../components/Deposit';
import Withdrawal from '../components/Withdrawal';
import VerificationForm from '../components/VerificationForm';
import '../styles/Dashboard.css'; // Import the CSS file

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <h2>Welcome to the Dashboard</h2>
      <AccountBalances />
      <CashierInfo />
      <Deposit />
      <Withdrawal />
      <VerificationForm />
      {/* Other dashboard components can go here */}
    </div>
  );
};

export default Dashboard;
