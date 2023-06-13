import React, { useState } from 'react';
import styles from './FAQSection.module.css';

const FAQSection = () => {
    const [selectedQuestion, setSelectedQuestion] = useState(null);

    const faqs = [
        { question: 'How do I make a reservation?', answer: 'To make a reservation, you can follow these steps...' },
        { question: 'What types of planes are available for reservation?', answer: 'We offer a wide range of planes including...' },
        { question: 'Can I choose my seat when reserving a plane?', answer: 'Yes, you can select your preferred seat during the reservation process...' },
        { question: 'What payment methods are accepted?', answer: 'We accept various payment methods such as credit cards, PayPal, and more...' },
        { question: 'Are there any discounts available for frequent flyers?', answer: 'Yes, we have a frequent flyer program that offers exclusive discounts...' },
        { question: 'Is there a cancellation policy?', answer: 'Our cancellation policy allows you to...' },
    ];

    return (
        <div className={styles.container}>
            <h2 className={styles.heading}>Frequently Asked Questions</h2>
            {faqs.map((faq, index) => (
                <div className={styles.faq} key={index}>
                    <p className={styles.question} onClick={() => setSelectedQuestion(index)}>
                        {faq.question}
                    </p>
                    {selectedQuestion === index && <p className={styles.answer}>{faq.answer}</p>}
                </div>
            ))}
        </div>
    );
}

export default FAQSection;
