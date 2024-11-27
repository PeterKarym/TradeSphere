// src/components/NavBar.js
import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/home">Home</Link></li>
        <li><Link to="/signup">Sign Up</Link></li>
        <li><Link to="/signin">Sign In</Link></li>
        <li><Link to="/profile">Profile</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/mt5-chart">MT5 Chart</Link></li>
        <li><Link to="/reports">Reports</Link></li>
      </ul>
    </nav>
  );
};

export default NavBar;
