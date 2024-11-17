import React from 'react';
import './InventoryAnalysis.css';
import Sidebar from '../Sidebar/Sidebar'

const InventoryAnalysis = () => {
  return (
    <div className="inventory-analysis-container">
        <Sidebar />
      <div className="content">
        <main className="main-content">
          <h2 className="main-title">Current Inventory Analysis</h2>
          <div className="metric-cards">
            <div className="metric-card purple">
              <h3>30,000</h3>
              <p>Total items</p>
              <span className="growth">⬆ 12%</span>
            </div>
            <div className="metric-card blue">
              <h3>270</h3>
              <p>Total orders</p>
              <span className="growth">⬆ 12%</span>
            </div>
            <div className="metric-card orange">
              <h3>1,000</h3>
              <p>Today's revenue</p>
              <span className="growth">⬆ 12%</span>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default InventoryAnalysis;
