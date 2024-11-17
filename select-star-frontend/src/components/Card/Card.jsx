import React from "react";
import "./Card.css";

const Card = ({ title, subheading, onClick }) => {
  return (
    <div className="dashboard-card" onClick={onClick}>
    <h3>{title}</h3>
    <p>{subheading}</p>
  </div>
  );
};

export default Card;
