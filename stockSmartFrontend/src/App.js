import './App.css';
import React, { useEffect, useState } from 'react';
import Dashboard from "./pages/Dashboard/Dashboard";
import Header from './components/Header/Header';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import InventoryAnalysis from './components/InventoryAnalysis/InventoryAnalysis';
import Login from './components/Login/login';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const ProtectedRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/login" />;
  };

  return (
    <Router>
    <div className="app">
      {isAuthenticated && <Header />}
      
      <Routes>
        <Route path="/login" element={isAuthenticated==true? <Header />:<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/" element={
            <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/inventory-analysis" element={
          <ProtectedRoute>
            <InventoryAnalysis />
          </ProtectedRoute>
        } />
      </Routes>    
    </div>
    </Router>
  );
}

export default App;
