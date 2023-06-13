import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFacebook, faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons'
import styles from './SocialMediaAndHours.module.css';

const SocialMediaAndHours = () => {
    return (
        <div className={styles.container}>
            <h2 className={styles.heading}>Follow Us</h2>
            <div className={styles.links}>
                <a className={styles.link} href="https://www.facebook.com/your_page">
                    <FontAwesomeIcon icon={faFacebook} size="2x" style={{ marginRight: '10px' }}/>
                    Facebook
                </a>
                <a className={styles.link} href="https://www.twitter.com/your_account">
                    <FontAwesomeIcon icon={faTwitter} size="2x" style={{ marginRight: '10px' }}/>
                    Twitter
                </a>
                <a className={styles.link} href="https://www.instagram.com/your_account">
                    <FontAwesomeIcon icon={faInstagram} size="2x" style={{ marginRight: '10px' }}/>
                    Instagram
                </a>
            </div>
            <h2 className={styles.heading}>Business Hours</h2>
            <p className={styles.hours}>Mon - Fri: 9AM - 5PM</p>
        </div>
    );
}

export default SocialMediaAndHours;
