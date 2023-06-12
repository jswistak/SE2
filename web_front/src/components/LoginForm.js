import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { callApi } from "../misc/Api";
import Cookies from "js-cookie";
import { useAuth } from "../misc/useAuth";

const LoginForm = (props) => {
    const [username, setUsername] = useState('');
    const [pass, setPass] = useState('');
    const {isLogged, setIsLogged} = useAuth();
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(username);
        const body = {
            username: username,
            password: pass
        }
        callApi("api/login/", "POST", body)
            .then(response => {
                console.log(response);
                const { refresh, access } = response;
                if (refresh && access) {
                    Cookies.set("refreshToken", refresh);
                    Cookies.set("accessToken", access);
                    setIsLogged(true);
                    navigate("/");
                }
            });
    }

    return (
        <div className="auth-form-container">
            <h2>Log In</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="username">username</label>
                <input value={username} onChange={(e) => setUsername(e.target.value)} type="username" placeholder="username" name="username"/>
                <label htmlFor="password">password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="*******"/>
                <button type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.changeForm('register')}>Don't have an account? Register here</button>
        </div>
    )
}

export default LoginForm;