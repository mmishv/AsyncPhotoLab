import React, { useState } from 'react';
import axios from 'axios';
import '../styles/Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('/auth/login/', {
        email,
        password,
      });

      localStorage.setItem('access_token',  JSON.stringify(response.data) );

      console.log(response.data);
      window.location.href = '/tasks';
    } catch (error) {
      console.error(error.response.data);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        </label>
        <br />
        <label>
          Password:
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
        </label>
        <br />
        <button type="submit" className="login-button">Log In</button>
      </form>
    </div>
  );
}

export default Login;
