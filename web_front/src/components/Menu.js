import React, { useContext } from "react";
import styles from "./Menu.module.css";
import { IsMobileContext } from "../App.js";
import { useNavigate } from "react-router-dom";

function Menu({ links, isMenuOpen, isSticky, menuRef, menuButton }) {
  const isMobile = useContext(IsMobileContext);
  const navigate = useNavigate();
  
  const navClassName = `${styles.nav} ${isSticky ? styles.sticky : ''} ${isMenuOpen ? styles.active : ''} ${isMobile ? styles.mobile : ''}`;
  const navListClassName = `${styles["nav-list"]} ${isMenuOpen ? styles.active : ''} ${isMobile ? styles.mobile : ''} ${isSticky ? styles.sticky : ''}`;
  console.log(links);
  
  return (
    <nav className={navClassName} ref={menuRef}>
      <ul className={navListClassName}>
        {links.map((link, index) => (
          <li key={index} className={styles["nav-item"]}>
            <button className={styles["nav-link"]} onClick={() => navigate(link.href)}>
              {link.text}
            </button>
          </li>
        ))}
      </ul>
      {menuButton}
    </nav>
  );
}

export default Menu;