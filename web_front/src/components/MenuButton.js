import React from "react";

function MenuButton({ isActive, toggleMenu, toggleRef }) {
  return (
    <div
      className={`toggle ${isActive ? "active" : ""}`}
      ref={toggleRef}
      onClick={toggleMenu}
    />
  );
}

export default MenuButton;