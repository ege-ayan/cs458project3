import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import NearestSea from './NearestSea';
import DistanceToSun from './DistanceToSun';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>

        <Route path="/" element={<LoginPage />} />


        <Route path="/nearest-sea" element={<NearestSea />} />


        <Route path="/distance-to-sun" element={<DistanceToSun />} />


        <Route path="*" element={<div>Page not found</div>} />
      </Routes>
    </Router>
  );
}

export default App;
