import React, { useState } from "react";
import { callApi } from "../misc/Api";

const RegisterForm = (props) => {
    const [email, setEmail] = useState('');
    const [pass, setPass] = useState('');
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [username, setUsername] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
        const user = {
            username: username,
            email: email,
            password: pass,
            first_name: name,
            last_name: surname,
        };
        console.log(JSON.stringify(user));
        // Make a POST request to your backend API
        callApi("api/register/", "POST", user)
        .then(data => {
            // Handle the response from the backend
            console.log(data);
            // Perform any necessary actions or show a success message to the user
        })
        .catch(error => {
            // Handle any errors that occurred during the request
            console.error(error);
            // Show an error message to the user or perform any necessary actions
        });
    }

    return (
        <div className="auth-form-container"> 
            <h2>Register</h2>
            <form className="register-form" onSubmit={handleSubmit}>
                <label htmlFor="username">username</label>
                <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="username" name="username"/>
                <label htmlFor="name">first name</label>
                <input value={name} onChange={(e) => setName(e.target.value)} placeholder="first name" name="name"/>
                <label htmlFor="surname">last name</label>
                <input value={surname} onChange={(e) => setSurname(e.target.value)} placeholder="last name" name="surname"/>
                <label htmlFor="email">email</label>
                <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="email@mail.com" name="email"/>
                <label htmlFor="password">password</label>
                <input value={pass} onChange={(e) => setPass(e.target.value)} type="password" placeholder="*******"/>
                <button type="submit">Register</button>
            </form>
            <button className="link-btn" onClick={() => props.changeForm('login')}>Already have an account? Login here</button>
        </div>
    )
}

export default RegisterForm;