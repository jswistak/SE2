import React, { useState, useRef, useEffect } from "react";
import hero from "../resources/images/hero-plane.jpg";
import HeroImage from "./HeroImage";
import Logo from "./Logo";
import MenuButton from "./MenuButton";
import Nav from "./Nav";

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isSticky, setIsSticky] = useState(false);
  const [isAtTop, setIsAtTop] = useState(true);

  const toggleRef = useRef(null);
  const navRef = useRef(null);
  const headerRef = useRef(null);

  const toggleMenu = () => {
    setIsMenuOpen((prevState) => !prevState);
  };

  const handleScroll = () => {
    const isAtTop = window.scrollY === 0;
    setIsAtTop(isAtTop);
    setIsSticky(!isAtTop);

    const nav = navRef.current;
    if (nav && isAtTop) {
      nav.classList.toggle("active", false);
    }

    const toggle = toggleRef.current;
    if (toggle && isAtTop) {
      toggle.classList.toggle("active", false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const headerClass = isSticky ? "sticky" : "";

  const links = [
    { href: "#", text: "Home" },
    { href: "#", text: "Profile" },
    { href: "#", text: "Team" },
    { href: "#", text: "Contact" },
    { href: "Login", text: "Login" }
  ];

  return (
    <header className={headerClass} ref={headerRef}>
      <HeroImage src={hero} />
      <Logo phrase="Roam!"/>
      <MenuButton
        isActive={isMenuOpen}
        toggleMenu={toggleMenu}
        toggleRef={toggleRef}
      />
      <Nav links={links} isActive={isMenuOpen} navRef={navRef} />
    </header>
  );
}

export default Header;
