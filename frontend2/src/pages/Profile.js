// src/pages/Profile.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const Profile = () => {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    console.log('Fetching user details...');
    axios.get('http://localhost:8000/api/user/', { withCredentials: true })
      .then(response => {
        console.log('User details fetched:', response.data);
        setUser(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the user details!', error);
      });
  }, []);

  const initialValues = {
    username: user?.username || '',
    email: user?.email || '',
    password: '',
  };

  const validationSchema = Yup.object({
    username: Yup.string().required('Required'),
    email: Yup.string().email('Invalid email format').required('Required'),
    password: Yup.string(),
  });

  const onSubmit = (values) => {
    axios.put('http://localhost:8000/api/user/', values, { withCredentials: true })
      .then(response => {
        setMessage('User details updated successfully');
        setUser({ ...user, ...values, password: '' });
      })
      .catch(error => {
        setMessage('There was an error updating the user details');
        console.error('There was an error updating the user details!', error);
      });
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Profile</h2>
      <Formik initialValues={initialValues} validationSchema={validationSchema} onSubmit={onSubmit} enableReinitialize>
        <Form>
          <div>
            <label htmlFor="username">Username</label>
            <Field type="text" id="username" name="username" autoComplete="username" />
            <ErrorMessage name="username" component="div" />
          </div>
          <div>
            <label htmlFor="email">Email</label>
            <Field type="email" id="email" name="email" autoComplete="email" />
            <ErrorMessage name="email" component="div" />
          </div>
          <div>
            <label htmlFor="password">New Password (leave blank to keep current password)</label>
            <Field type="password" id="password" name="password" autoComplete="new-password" />
            <ErrorMessage name="password" component="div" />
          </div>
          <button type="submit">Update</button>
        </Form>
      </Formik>
      {message && <div>{message}</div>}
    </div>
  );
};

export default Profile;
