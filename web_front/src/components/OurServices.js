import React from "react";
import styles from './OurServices.module.css';
import ImageInternationalTravel from "../resources/images/international-travel.png";
import ImageLuxuryTravel from "../resources/images/luxury-travel.png";
import ImageCharterFlights from "../resources/images/charter-flight.png";

const OurServices = () => {
    return (
        <section className={styles.services}>
            <h2>Our Services</h2>
            <div className={styles.grid}>
                <div className={`${styles.card} ${styles.long}`}>
                    <img src={ImageInternationalTravel} alt="icon1"/>
                    <h3>Domestic and International Travel</h3>
                    <p>We cover a wide array of local and international destinations to get you where you need to be.</p>
                </div>
                <div className={`${styles.card} ${styles.short} ${styles.marginTop}`}>
                    <img src={ImageLuxuryTravel} alt="icon2"/>
                    <h3>Luxury Travel Packages</h3>
                    <p>Experience travel like never before with our deluxe packages offering first-class amenities and exclusive privileges.</p>
                </div>
                <div className={`${styles.card} ${styles.long} ${styles.marginTop}`}>
                    <img src={ImageCharterFlights} alt="icon3"/>
                    <h3>Group Charters</h3>
                    <p>Need to travel in a group? We have you covered with our reliable and convenient group charter services.</p>
                </div>
            </div>
        </section>
    );
}

export default OurServices;
