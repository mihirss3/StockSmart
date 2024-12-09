import React from "react";
import "./Dashboard.css";
import homepageImage from '../../assets/images/homepageImage.jpg'
import Card from "../../components/Card/Card";
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();
    const handleFirstCardClick = () => {
        console.log('clicked')
        navigate('/inventory-analysis');
      };

  return (
    <main className="dashboard">
        <div className="dashboard-layout1">
            <div className="dashboard-headings-info">
            <h1 className="dashboard-title">
            Data-Driven Forecasting and Visualization of Fresh Food Demand
            </h1>
            <p className="dashboard-subheading">
                        This is all about changing how inventory is managed by using historical sales data to 
                    predict what fresh food items will be in demand. By using data-driven approach through 
                    machine learning and advanced data visualization, the system provides retail stores with 
                    accurate insights into buying patterns and what they need to stock up on. It's a centralized 
                    platform where analysts can keep an eye on inventory levels, track how products are 
                    selling, and spot trends as they happen, helping stores make smarter decisions. 
                    
                    This platform will help stores keep the right number of products in stock, reducing waste 
                    and supporting sustainability. By offering real-time demand forecasting and interactive 
                    visual dashboards, it aims to make operations smoother, increase profits, and ensure 
                    customers always find fresh products on the shelves. The easy-to-use interface, along with 
                    these data-driven insights, will allow stores to adjust their inventory and marketing 
                    strategies proactively, boosting efficiency and customer satisfaction. 
            </p>
            </div>
            <img className="dashboard-image" src={homepageImage} alt="homepageImage"></img>
        </div>
    
      <div className="dashboard-cards">
        <Card title="Current Inventory Analysis and Demand Forecast" onClick={handleFirstCardClick}/>
        {/* <Card title="Demand Forecast" /> */}

      </div>
    </main>
  );
};

export default Dashboard;
