
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Dashboard from "./pages/Dashboard/Dashboard";
import Header from './components/Header/Header';
// import Sidebar from './components/Sidebar/Sidebar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import InventoryAnalysis from './components/InventoryAnalysis/InventoryAnalysis';

function App() {
  const [helloMessage, setHelloMessage] = useState('');
  const [worldMessage, setWorldMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/hello')
      .then(response => {
        setHelloMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the 'hello' message!", error);
      });

    axios.get('http://127.0.0.1:8000/world')
      .then(response => {
        setWorldMessage(response.data.message);
      })
      .catch(error => {
        console.error("There was an error fetching the 'world' message!", error);
      });
  }, []);

 console.log(helloMessage);
 console.log(worldMessage);

  return (
    <Router>
    <div className="app">
      <Header />
      
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/inventory-analysis" element={<InventoryAnalysis />} />
      </Routes>
   
       {/* <Sidebar /> */}
    
    </div>
    </Router>
  );
}

export default App;
