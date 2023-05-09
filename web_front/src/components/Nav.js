import React from "react";

function Nav({ links, isActive, navRef }) {
  return (
    <nav className={`${isActive ? "active" : ""}`} ref={navRef}>
      <ul>
        {links.map((link, index) => (
        <li key={index}>
          <a href={link.href}>
            {link.text}
          </a>
        </li>
      ))}
      </ul>
    </nav>
  );
}

export default Nav;