import React, { useState, useRef, useEffect, useContext } from 'react';
import hero from '../resources/images/hero-plane.jpg';
import { IsMobileContext } from "../App.js";
import './Header.css';
import styles from "./Header.module.css";
import HeroImage from './HeroImage';
import Logo from './Logo';
import MenuButton from './MenuButton';
import Menu from './Menu';
import { useAuth } from '../misc/useAuth';

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSticky, setIsSticky] = useState(false);
  const {isLogged, setIsLogged} = useAuth();
  console.log(isLogged);
  const menuButtonRef = useRef(null);
  const menuRef = useRef(null);
  const headerRef = useRef(null);

  const toggleMenu = () => {
    setIsMenuOpen((prevState) => !prevState);
  };

  const handleScroll = () => {
    const isAtTop = window.scrollY === 0;
    setIsSticky(!isAtTop);
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);
  //console.log(isLogged ? { href: "/Login", text: "Login"} : {href: "Logout", text: "Logout"});
  const links = [
    { href: "/#", text: "Home" },
    { href: "/Profile", text: "Profile" },
    { href: "/#", text: "Team" },
    { href: "/#", text: "Contact" },
    isLogged ? {href: "/Login", text: "Logout" } : {href: "/Login", text: "Login" }
  ];
  

  const isMobile = useContext(IsMobileContext);
  const mobileClass = isMobile ? styles.mobile : '';

  const headerClass = `${styles.header} ${isSticky ? styles.sticky : ''} ${mobileClass}`;
  const heroClass = `${styles.hero} ${isSticky ? styles.sticky : ''} ${mobileClass}`;
  const logoClass = `${styles.logo} ${isSticky ? styles.sticky : ''} ${mobileClass}`;


  return (
    <header className={headerClass} ref={headerRef}>
      <HeroImage className={heroClass} src={hero} />
      <Logo className={logoClass} background="white" phrase="Roam!" />
      <Menu
        links={links}
        isMenuOpen={isMenuOpen}
        isSticky={isSticky}
        menuRef={menuRef}
        menuButton={
          <MenuButton
            isMenuOpen={isMenuOpen}
            isSticky={isSticky}
            toggleMenu={toggleMenu}
            menuButtonRef={menuButtonRef}
            position={{ top: '15px', right: '40px' }}
            isMobileOnly={true}
          />
        }
      />
      <div className={styles['margin-bottom']}>
        {/* Header is position fixed. Necessary to independently set the baseline margin for other elements in the document flow */}
      </div>
    </header>
  );
}

export default Header;
