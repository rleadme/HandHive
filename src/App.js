
import React from 'react';
import Join from './component/Join';
import Home from './component/Home';
import Start from './component/Start';

// import Join from './component/Join';
import { BrowserRouter, Navigate, Router, Routes, Route, Link} from 'react-router-dom';




const App = () => {
  return (
   //  <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="Join" element={<Join />} />
        <Route path="Start" element={<Start />}/>
      </Routes>
    // </BrowserRouter>

  );
  
 
}

export default App;
