
import './App.css';
import Dashboard from "./pages/Dashboard/Dashboard";
import Header from './components/Header/Header';
// import Sidebar from './components/Sidebar/Sidebar';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import InventoryAnalysis from './components/InventoryAnalysis/InventoryAnalysis';

function App() {
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
