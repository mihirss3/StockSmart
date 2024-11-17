import React from "react";
import "./Header.css";
import { FaSearch, FaUserCircle } from "react-icons/fa";
import { TiThMenu } from "react-icons/ti";


const Header = () => {
  return (
    <header className="header">
      <div className="menu-icon">
      <TiThMenu />
      </div>
      <div className="search-bar">
      <FaSearch className="search-icon"/>
        <input className="search-bar-input" type="text" placeholder="Search" />
      </div>
      <div className="profile-icon">
      <FaUserCircle className="user-icon" />
      </div>
    </header>
  );
};

export default Header;
