import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import CompetitorsAnalysis from './components/Competitors/CompetitorsAnalysis';
import BusinessFeasibility from './components/BusinessFeasibility/BusinessFeasibility';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/competitors" element={<CompetitorsAnalysis />} />
          <Route path="/business-feasibility" element={<BusinessFeasibility />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
