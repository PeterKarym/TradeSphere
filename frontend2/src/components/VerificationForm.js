import React, { useState } from 'react';
import axios from 'axios';
import '../styles/VerificationForm.css';

const VerificationForm = () => {
  const [verificationCode, setVerificationCode] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/handle-email-verification/', {
        verification_code: verificationCode
      });
      setMessage(`Verification successful! ${response.data.message}`);
    } catch (error) {
      console.error('Verification failed:', error.response.data);
      setMessage('Failed to verify code.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="verification_code" className="bold-label">Verification Code:</label>
      <input
        type="text"
        id="verification_code"
        name="verification_code"
        value={verificationCode}
        onChange={(e) => setVerificationCode(e.target.value)}
        placeholder="Enter email verification code"
        required
      />
      <button type="submit">Verify Email</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default VerificationForm;
