import React, { useState } from 'react';
import './LoginPage.css';
import { GoogleLogin } from '@react-oauth/google';
import { getUserByEmailAndPassword } from './userData';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const performLoginLogic = (e) => {
    e.preventDefault();

    // Check Internet Connection (CASE 1)
    if (!navigator.onLine) {
      alert("No internet connection available.");
      return;
    }

    // Check if email or password is empty (CASE 2.1)
    if (!email.trim() || !password.trim()) {
      alert("Email and password are required.");
      return;
    }

    // Check if user is valid or not
    const user = getUserByEmailAndPassword(email, password);
    if (user) {
      // successful login (CASE 3)
      alert("Successfully logged in");
    } else { // CASE (2.2)
      alert("Invalid email or password");
    }
  }

  const responseMessage = (response) => { // CASE 4
    alert("Successfully logged in using Google Auth");
  };

  const errorMessage = (error) => { // CASE 5
    alert("Error logging in with Google Auth");
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Login</h2>
        <form>
          <div className="form-group">
            <label>Email:</label>
            <input type="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </div>
          <div className="login-button-container">
            <button className="login-button" onClick={performLoginLogic}>Login</button>
          </div>
        </form>
        <div className="google-login-button">
          <GoogleLogin 
            onSuccess={responseMessage} 
            onError={errorMessage} 
          />
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
