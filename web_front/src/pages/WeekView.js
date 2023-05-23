import React from 'react';
import styles from './WeekView.module.css';

const WeekView = ({ currentMonth, currentYear }) => {
    // Samples for demonstration:
    const events = [
        {
            day: 1,
            time: '09:00',
            title: 'Sample Event 1',
            description: 'This is a sample event description.',
        },
        {
            day: 3,
            time: '14:00',
            title: 'Sample Event 2',
            description: 'This is another sample event description.',
        },
    ];

    return (
        <div className={styles.week}>
            {events.map((event, index) => (
                <div key={index} className={styles.event}>
                    <div className={styles.day}>Day {event.day}</div>
                    <div className={styles.time}>{event.time}</div>
                    <div className={styles.title}>{event.title}</div>
                    <div className={styles.description}>{event.description}</div>
                </div>
            ))}
        </div>
    );
};

export default WeekView;
