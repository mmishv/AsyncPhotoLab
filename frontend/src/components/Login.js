import React, { useState } from 'react';
import axios from 'axios';
import '../styles/Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const token = btoa(`${email}:${password}`);
      const response = await axios.post('/login/', {}, {
        headers: {
          Authorization: `Basic ${token}`,
        }
      });

       localStorage.setItem('access_token', JSON.stringify(response.data.access_token));
       localStorage.setItem('user_email', email);

      console.log(response.data);
      window.location.href = '/';
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
