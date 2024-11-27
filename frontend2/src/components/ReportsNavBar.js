import React from 'react';
import { Link } from 'react-router-dom';

const ReportsNavBar = () => {
  return (
    <nav className="reports-nav">
      <ul>
        <li><Link to="/reports/trades">Trades Report</Link></li>
        <li><Link to="/reports/strategy">Strategy Report</Link></li>
        <li><Link to="/reports/mt5">MT5 Report</Link></li>
        <li><Link to="/reports/transactions">Transactions Report</Link></li>
      </ul>
    </nav>
  );
};

export default ReportsNavBar;
