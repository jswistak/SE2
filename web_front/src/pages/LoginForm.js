import React, { useState } from "react";

const LoginForm = (props) => {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
    }

    return (
        <div className="auth-form-container">
            <h2>Log In</h2>
            <form className="login-form" onSubmit={handleSubmit}>
                <label htmlFor="email">email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="email@mail.com" name="email"/>
                <label htmlFor="password">password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="*******"/>
                <button type="submit">Log In</button>
            </form>
            <button className="link-btn" onClick={() => props.changeForm('register')}>Don't have an account? Register here</button>
        </div>
    )
}

export default LoginForm;