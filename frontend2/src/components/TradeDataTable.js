// src/components/TradeDataTable.js
import React from 'react';

const TradeDataTable = () => {
  return (
    <table className="trade-data-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Time</th>
          <th>Trade Type</th>
          <th>Price</th>
          <th>Lot Size</th>
          <th>Stop Loss</th>
          <th>Target Profit</th>
          <th>Risk:Reward</th>
          <th>Profit/Loss</th>
        </tr>
      </thead>
      <tbody>
        {/* Rows with trade data will be added dynamically here */}
      </tbody>
    </table>
  );
};

export default TradeDataTable;
