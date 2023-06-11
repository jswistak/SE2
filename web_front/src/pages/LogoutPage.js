import React, { useState } from "react";
import './LoginPage.css'
import { useAuth } from "../misc/useAuth";
import { useNavigate } from "react-router-dom";

const LogoutPage = (props) => {
    const navigate = useNavigate();
    const {isLogged, setIsLogged} = useAuth();

    const handleLogout = () => {
        setIsLogged(false);
        navigate("/");
      };
    return(
        <div className="LoginPage">
            <form className="login-form" onSubmit={handleLogout}>
                <label>Are you sure you want to logout?</label>
                <button type="submit">Yes</button>
                <button onClick={navigate("/")}>No</button>
            </form>
            
        </div>
    );
}

export default LogoutPage;