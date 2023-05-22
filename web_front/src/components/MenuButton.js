import React, { useContext } from 'react';
import styles from "./MenuButton.module.css";
import menuIcon from "../resources/icon-set/icon-menu.svg";
import closeIcon from "../resources/icon-set/icon-close.svg";
import { IsMobileContext } from "../App.js";

function MenuButton({ isMenuOpen, isSticky, toggleMenu, menuButtonRef, position, isMobileOnly }) {

  const isMobile = useContext(IsMobileContext);
  const buttonClass = isSticky && (isMobileOnly ? isMobile : false) ? styles.button : "";
  const buttonIconClass = isMenuOpen ? styles["button-close"] : styles["button-menu"];
  console.log(isMenuOpen ? 'menu otwarte' : 'menu zamkniete');

  /* MenuButton position is fixed */
  const positionStyle = {
    top: position.top,
    right: position.right,
  };

  const iconStyle = {
    '--menu-icon': `url(${menuIcon})`,
    '--close-icon': `url(${closeIcon})`,
  };

  return (
    <div
      className={`${buttonClass} ${buttonIconClass}`}
      ref={menuButtonRef}
      onClick={toggleMenu}
      style={{ ...positionStyle, ...iconStyle }}
    />
  );
}

export default MenuButton;