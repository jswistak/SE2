import React, { useState } from "react";
import './LoginPage.css'
import { useAuth } from "../misc/useAuth";
import { useNavigate } from "react-router-dom";

const LogoutPage = (props) => {
    const navigate = useNavigate();
    const {isLogged, setIsLogged} = useAuth();
    const [confirm, setConfirm] = useState(false);
    const handleLogout = () => {
        setIsLogged(false);
        navigate("/");
      };
    const handleCancel = () => {
        setIsLogged(true);
        navigate("/");
    }
    return(
        <div className="LoginPage">
            <label>Are you sure you want to logout?</label>
            <button onClick={handleLogout}>Yes</button>
            <button onClick={handleCancel}>No</button>  
        </div>
    );
}

export default LogoutPage;