import React from 'react';
import { FaPhone, FaEnvelope, FaMapMarkerAlt } from 'react-icons/fa';
import styles from './ContactInfo.module.css';

const ContactInfo = () => {
    return (
        <div className={styles.container}>
            <h2 className={styles.heading}>Contact Information</h2>
            <div className={styles.info}>
                <FaPhone size="1.5em" />
                <p className={styles.infoText}>+48 234 567 890</p>
            </div>
            <div className={styles.info}>
                <FaEnvelope size="1.5em" />
                <p className={styles.infoText}>contact@roam.com</p>
            </div>
            <div className={styles.info}>
                <FaMapMarkerAlt size="1.5em" />
                <p className={styles.infoText}>Noakowskiego 1234, Warsaw, Poland</p>
            </div>
        </div>
    );
}

export default ContactInfo;
