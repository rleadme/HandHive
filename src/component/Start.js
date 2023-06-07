import React, { useState } from 'react';
import thema from './assets/thema.png';
import './Home.css';
import {Webcam} from 'react-webcam'

const Start = () => {
 


  return (
    <div class="App-header">

        {/* <img src={thema} className="App-thema" alt="thema" /> */}
         
         <div class = "Start-cam"> 
         <p>
           WebCam
          </p>
          <Webcam />
          </div>
      
  
    </div>
  );
}

export default Start;
