import React from "react";
import Header from "../components/Header"
import ContactInfo from "../components/ContactInfo"
import AboutUs from "../components/AboutUs";
import OurServices from "../components/OurServices";
import Testimonials from "../components/Testimonials";

const HomePage = (props) => {
    return (
    <div>
        <Header />
        <AboutUs />
        <OurServices />
        <Testimonials />
        <ContactInfo />
    </div>
    );
}

export default HomePage;