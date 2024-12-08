import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css';
import axios from 'axios';

const Login = ({ setIsAuthenticated }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/login', {
                emailId: email,
                password: password
            });
    
            if (response.data.success) {
                setIsAuthenticated(true);
                navigate('/');
            }
        } catch (error) {
            alert(error.response?.data?.message || 'Invalid credentials');
        }
    };

    return (
        <div className="login-container">
            <div className="login-left">
                <h1 className="login-title">StockSmart</h1>
                <p className="login-subtitle">Data-Driven Forecasting and Visualization of Fresh Food Demand</p>
            </div>
            <div className="login-form">
                <form onSubmit={handleLogin}>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                    <button type="submit" className="sign-in-button">Sign In</button>
                </form>
            </div>
        </div>
    );
};

export default Login;