import React, { useContext } from "react";
import styles from "./Menu.module.css";
import { IsMobileContext } from "../App.js";

function Menu({ links, isMenuOpen, isSticky, menuRef, menuButton }) {
  const isMobile = useContext(IsMobileContext);

  const navClassName = `${styles.nav} ${isSticky ? styles.sticky : ''} ${isMenuOpen ? styles.active : ''} ${isMobile ? styles.mobile : ''}`;
  const navListClassName = `${styles["nav-list"]} ${isMenuOpen ? styles.active : ''} ${isMobile ? styles.mobile : ''} ${isSticky ? styles.sticky : ''}`;

  return (
    <nav className={navClassName} ref={menuRef}>
      <ul className={navListClassName}>
        {links.map((link, index) => (
          <li key={index} className={styles["nav-item"]}>
            <a href={link.href} className={styles["nav-link"]}>
              {link.text}
            </a>
          </li>
        ))}
      </ul>
      {menuButton}
    </nav>
  );
}

export default Menu;
