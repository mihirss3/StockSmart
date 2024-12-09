import React from "react";
import "./Header.css";
import { useNavigate } from 'react-router-dom';


const Header = ({setIsAuthenticated}) => {
  const navigate = useNavigate();

  return (
    <header className="header">
      <button className="logout-button" onClick={()=> {setIsAuthenticated(false); navigate('/')}}>Log Out</button>

    </header>
  );
};

export default Header;
