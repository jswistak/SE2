import React, { useState } from 'react';
import styles from './Calendar.module.css';
import { callApi } from "../misc/Api";


const Calendar = () => {
    const currentDate = new Date();
    const [currentMonth, setCurrentMonth] = useState(currentDate.getMonth());
    const [currentYear, setCurrentYear] = useState(currentDate.getFullYear());
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    const [bookedDays, setBookedDays] = useState({});

    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const changeMonth = (delta) => {
        let newMonth = currentMonth + delta;
        let newYear = currentYear;

        if (newMonth < 0) {
            newMonth = 11;
            newYear--;
        } else if (newMonth > 11) {
            newMonth = 0;
            newYear++;
        }



        setCurrentMonth(newMonth);
        setCurrentYear(newYear);


    };

    const bookDay = (day) => {
        const startTime = new Date(currentYear, currentMonth, day, 9, 0, 0).toISOString();
    const endTime = new Date(currentYear, currentMonth, day, 11, 0, 0).toISOString();

    const bookingData = {
        aircraft: aircraftId,
        pilot: pilotId,
        instructor: instructorId,
        start_time: startTime,
        end_time: endTime,
    };

    callApi('api/booking/', 'POST', bookingData)
        .then(data => {
            //Update the bookedDays state with the new booking.
            const eventTitle = `${data.aircraft.aircraft_id} - ${data.start_time} - ${data.end_time}`;
            const eventDescription = `Pilot: ${data.pilot.username}\nInstructor: ${data.instructor.username}`;
            setBookedDays({
                ...bookedDays,
                [day]: { title: eventTitle, description: eventDescription },
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };

    const days = [];
    for (let i = 1; i <= daysInMonth; i++) {
        const eventDetails = bookedDays[i];

        days.push(
            <div
                key={i}
                className={`${styles['calendar-day']} ${eventDetails ? styles.booked : ''}`}
                onClick={() => {
                    if (!eventDetails) {
                        bookDay(i);
                    }
                }}
            >
                {i}
                {eventDetails && (
                    <div className={styles.tooltip}>
                        <strong>{eventDetails.title}</strong>
                        <br />
                        {eventDetails.description}
                    </div>
                )}
            </div>
        );
    }

    return (
        <div>
            <div className={styles.navigation}>
                <button onClick={() => changeMonth(-1)}>&lt;</button>
                <span>{monthNames[currentMonth]} {currentYear}</span>
                <button onClick={() => changeMonth(1)}>&gt;</button>
            </div>
            <div className={styles.calendar}>{days}</div>
        </div>
    );
};

export default Calendar;
