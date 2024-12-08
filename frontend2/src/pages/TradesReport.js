import React from 'react';
import Volatility10Index from './Volatility10Index';
import Volatility25Index from './Volatility25Index';
import Volatility25OneSIndex from './Volatility25OneSIndex';
import Volatility50Index from './Volatility50Index';
import Volatility75Index from './Volatility75Index';
import Volatility100Index from './Volatility100Index';
import XAUUSD from './XAUUSD';

const TradesReport = () => {
  return (
    <div>
      <h2>Trades Report</h2>
      <div className="trades-report-section">
        <Volatility10Index />
      </div>
      <div className="trades-report-section">
        <Volatility25Index />
      </div>
      <div className="trades-report-section">
        <Volatility25OneSIndex />
      </div>
      <div className="trades-report-section">
        <Volatility50Index />
      </div>
      <div className="trades-report-section">
        <Volatility75Index />
      </div>
      <div className="trades-report-section">
        <Volatility100Index />
      </div>
      <div className="trades-report-section">
        <XAUUSD />
      </div>
    </div>
  );
};

export default TradesReport;
