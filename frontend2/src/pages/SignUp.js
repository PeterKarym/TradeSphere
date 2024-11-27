// src/pages/SignUp.js
import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

const SignUp = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  const initialValues = {
    username: '',
    email: '',
    password: '',
  };

  const validationSchema = Yup.object({
    username: Yup.string().required('Required'),
    email: Yup.string().email('Invalid email format').required('Required'),
    password: Yup.string().required('Required'),
  });

  const onSubmit = (values) => {
    axios.post('http://localhost:8000/api/register/', values)
      .then(response => {
        console.log('User registered successfully:', response);
        setMessage(response.data.message);
        navigate('/signin'); // Redirect to Sign In page after successful registration
      })
      .catch(error => {
        console.error('There was an error registering the user:', error);
        setMessage('There was an error registering the user!');
      });
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit}>
        <Form>
          <div>
            <label htmlFor="username">Username</label>
            <Field type="text" id="username" name="username" />
            <ErrorMessage name="username" component="div" />
          </div>
          <div>
            <label htmlFor="email">Email</label>
            <Field type="email" id="email" name="email" />
            <ErrorMessage name="email" component="div" />
          </div>
          <div>
            <label htmlFor="password">Password</label>
            <Field type="password" id="password" name="password" />
            <ErrorMessage name="password" component="div" />
          </div>
          <button type="submit">Sign Up</button>
        </Form>
      </Formik>
      {message && <p>{message}</p>} {/* Display message */}
      <p>Already have an account? <Link to="/signin">Sign in</Link></p> {/* Add link to Sign In */}
    </div>
  );
};

export default SignUp;
