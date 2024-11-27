import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ReportsNavBar from '../components/ReportsNavBar';
import TradesReport from './TradesReport';
import StrategyReport from './StrategyReport';
import MT5Report from './MT5Report';
import TransactionsReport from './TransactionsReport';

const Reports = () => {
  return (
    <div>
      <h2>Reports</h2>
      <ReportsNavBar />
      <Routes>
        <Route path="trades" element={<TradesReport />} />
        <Route path="strategy" element={<StrategyReport />} />
        <Route path="mt5" element={<MT5Report />} />
        <Route path="transactions" element={<TransactionsReport />} />
        <Route path="/" element={<Navigate to="trades" />} />
      </Routes>
    </div>
  );
};

export default Reports;
