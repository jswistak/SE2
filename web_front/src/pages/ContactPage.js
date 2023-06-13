import React from "react";
import Header from "../components/Header"
import ContactForm from "../components/ContactForm"
import ContactInfo from "../components/ContactInfo"
import SocialMediaAndHours from "../components/SocialMediaAndHours"
import FAQSection from "../components/FAQSection"

const ContactPage = (props) => {
    return (
    <div>
        <Header sticky={true}/>
        <ContactForm />
        <ContactInfo />
        <SocialMediaAndHours />
        <FAQSection />
    </div>
    );
}

export default ContactPage;