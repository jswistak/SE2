import React from "react";

function Logo({ className, background, phrase }) {

  const logoStyle = {
    background: background,
    WebkitBackgroundClip: "text",
    color: "transparent",
  };

  return (
    <a href="#" className={`${className}`} style={logoStyle}>
      <span>{phrase}</span>
    </a>
  );
}

export default Logo;
