import './App.css';
import React, { useState } from 'react';
import Dashboard from "./pages/Dashboard/Dashboard";
import Header from './components/Header/Header';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import InventoryAnalysis from './components/InventoryAnalysis/InventoryAnalysis';
import Login from './components/Login/login';
import AdminPortal from './components/AdminPortal/AdminPortal';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const ProtectedRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/" />;
  };

  return (
    <Router>
    <div className="app">
      {isAuthenticated && <Header setIsAuthenticated={setIsAuthenticated}/>}
      
      <Routes>
        <Route path="/admin-portal" element={<ProtectedRoute><AdminPortal /></ProtectedRoute>} />
        <Route path="/" element={isAuthenticated===true? <Header />:<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/analyst-dashboard" element={
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
