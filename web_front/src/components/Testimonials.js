import React, { useState, useEffect } from "react";
import styles from './Testimonials.module.css';

const testimonialsData = [
    {name: 'John Doe', testimonial: 'The flight was comfortable and punctual. Highly recommend!'},
    {name: 'Jane Smith', testimonial: 'Great service! The staff was really attentive and polite.'},
    {name: 'George Brown', testimonial: 'The amenities were top-notch. Definitely flying with them again!'}
];

const Testimonials = () => {
    const [activeIndex, setActiveIndex] = useState(0);

    useEffect(() => {
        const intervalId = setInterval(() => {
            setActiveIndex((activeIndex + 1) % testimonialsData.length);
        }, 4000); // Increase delay to 4 seconds to allow 1 second for the animation
    
        return () => clearInterval(intervalId);
    }, [activeIndex]);

    return (
        <section className={styles.testimonials}>
            <h2>Testimonials</h2>
            <div className={styles.testimonial}>
                <div key={activeIndex} className={styles.testimonial}>
                    <p>{testimonialsData[activeIndex].testimonial}</p>
                    <h3>- {testimonialsData[activeIndex].name}</h3>
                </div>
            </div>
        </section>
    );
}

export default Testimonials;
