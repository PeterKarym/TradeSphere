// src/pages/SignIn.js
import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const SignIn = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  const initialValues = {
    username: '',
    password: '',
  };

  const validationSchema = Yup.object({
    username: Yup.string().required('Required'),
    password: Yup.string().required('Required'),
  });

  const onSubmit = (values) => {
    axios.post('http://localhost:8000/api/login/', values)
      .then(response => {
        console.log('User logged in successfully:', response);
        setMessage(response.data.message);
        navigate('/dashboard');
      })
      .catch(error => {
        console.error('There was an error logging in the user:', error);
        setMessage('There was an error logging in the user!');
      });
  };

  return (
    <div>
      <h2>Sign In</h2>
      <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
        <Form>
          <div>
            <label htmlFor="username">Username</label>
            <Field type="text" id="username" name="username" />
            <ErrorMessage name="username" component="div" />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <Field type="password" id="password" name="password" />
            <ErrorMessage name="password" component="div" />
          </div>
          <button type="submit">Sign In</button>
        </Form>
      </Formik>
      {message && <p>{message}</p>} {/* Display message */}
      <p>Don't have an account? <Link to="/signup">Sign up</Link></p> {/* Add link to Sign Up */}
    </div>
  );
};

export default SignIn;
