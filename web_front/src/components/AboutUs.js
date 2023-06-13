import React from "react";
import styles from './AboutUs.module.css';

const AboutUs = () => {
    return (
        <section className={styles.parallax}>
            <div className={styles.cloud}></div>
            <div className={styles.content}>
                <h2>About Us</h2>
                <p>
                    We are a leading airline company offering the best flight experiences to our customers. Our fleet comprises the latest models, ensuring comfort, safety, and reliability. We strive to make your travel memorable.
                </p>
            </div>
        </section>
    );
}

export default AboutUs;
