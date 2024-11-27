import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import Profile from './pages/Profile';
import Dashboard from './pages/Dashboard';
import NavBar from './components/NavBar';
import Home from './pages/Home';
import MT5Chart from './pages/MT5Chart';
import Reports from './pages/Reports';
import './App.css';
import axios from 'axios';

// Configure Axios Defaults
axios.defaults.withCredentials = true;

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>TradeSphere</h1>
          <NavBar />  {/* Add NavBar component here */}
        </header>
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/mt5-chart" element={<MT5Chart />} />
          <Route path="/reports/*" element={<Reports />} /> {/* Update route for Reports */}
          <Route path="/" element={<Navigate to="/signin" />} />
          <Route path="*" element={<h2>404: Page Not Found</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
