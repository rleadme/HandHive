import React, {useState, useEffect} from 'react';
// import {Join} from './index.js'
//import exios from 'axios';

// function Login() {
//     const [inputId, setInputId = useState('')]
// }import React, { useState } from 'react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here, you can perform the login logic
    console.log('Email:', email);
    console.log('Password:', password);
    // Reset form fields
    setEmail('');
    setPassword('');
  };

  const handleJoinClick = () => {
    // Handle join button click event here
    console.log('Join button clicked!');
    // Perform any additional actions or page transitions
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </div >
    
        {/* <Link to="/join"><button type="Join" style={{margin: 5}}>Join</button></Link>
        <button type="submit" style={{margin: 5}}>Login</button> */}
       
      </form>
    </div>
  );
};

export default Login;
