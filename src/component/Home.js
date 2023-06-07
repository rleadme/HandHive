import React, {useState} from 'react';
import Login from './Login';
import './Home.css';
import thema from './assets/thema.png';
import { BrowserRouter, Navigate, Router, Routes, Route, Link} from 'react-router-dom';
const Home = () => {
    return (
      
        <div className="App">
          <header className="App-header">
    
    <div calss="App-wrap">
        <dlv class = "App-bg">
        <img src={thema} className="App-thema" alt="thema" />
          
          <head className="App-head">
             <p>
              Rock-Scissor-Paper!
            </p>
          </head>
    
          <dlv class = "App-Login">
          <Login />
          </dlv>

          <div class = "Home-button">
          <Link to="/join">
            <button type="Join" style={{margin: 5}}>Join</button>
            </Link>
          <Link to="/Start">
            <button type="submit" style={{margin: 5}}>Login</button>
            </Link>
          </div>

        </dlv> 
    </div>
    
  
          </header>
        </div>
    )
  }

export default Home;