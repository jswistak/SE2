import React, { useState } from 'react';
import styles from './ContactForm.module.css';

const ContactForm = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // handle form submission...
    };

    return (
        <form className={styles.form} onSubmit={handleSubmit}>
            <div className={styles.inputGroup}>
                <input 
                    className={`${styles.inputField} ${name && styles.hasValue}`} 
                    type="text" 
                    name="name" 
                    value={name} 
                    onChange={e => setName(e.target.value)} 
                    required 
                />
                <label className={styles.inputLabel}>Name</label>
            </div>
            <div className={styles.inputGroup}>
                <input 
                    className={`${styles.inputField} ${email && styles.hasValue}`} 
                    type="text" 
                    name="email" 
                    value={email} 
                    onChange={e => setEmail(e.target.value)} 
                    required 
                />
                <label className={styles.inputLabel}>Email</label>
            </div>
            <div className={styles.inputGroup}>
                <textarea 
                    className={`${styles.inputField} ${styles.textarea} ${message && styles.hasValue}`} 
                    name="message" 
                    value={message} 
                    onChange={e => setMessage(e.target.value)} 
                    required 
                />
                <label className={styles.inputLabel}>Message</label>
            </div>
            <input className={styles.submitButton} type="submit" value="Submit" />
        </form>
    );
}

export default ContactForm;
