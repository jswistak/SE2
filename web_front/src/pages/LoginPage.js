import React, { useState } from "react";
import LoginForm from "../components/LoginForm";
import RegisterForm from "../components/RegisterForm";
import './LoginPage.css'

const LoginPage = (props) => {
    const [currentForm, setCurrentForm] = useState(props.currentForm);

    const toggleForm = (formName) => {
        setCurrentForm(formName);
    }
    return(
        <div className="LoginPage">
            {currentForm === 'login' ? <LoginForm changeForm={toggleForm}/> : <RegisterForm changeForm={toggleForm}/>}
        </div>
    );
}

export default LoginPage;