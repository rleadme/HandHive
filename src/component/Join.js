import React, { useState } from 'react';
import thema from './assets/thema.png';
import './Home.css';

const Join = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleNameChange = (e) => {
    setName(e.target.value);
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };
 
  const handleSubmit = (e) => {
    e.preventDefault();
    // Here, you can perform the sign-up logic
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Password:', password);
    // Reset form fields
    setName('');
    setEmail('');
    setPassword('');
  };

  return (
    <div class = "App-header">
        <dlv class = "App-wrap">
        <dlv class = "App-bg">
        <img src={thema} className="App-thema" alt="thema" />
         
          <div class = "Join-form">
      <h2>회원가입</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={handleNameChange}
          />
        </div>
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
        </div>
      
        <button type="submit">Join</button>
        
      </form>
      </div>
      
      </dlv>
      </dlv>
    </div>
  );
};

export default Join;
