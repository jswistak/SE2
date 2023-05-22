import React from "react";

function Logo({ className, phrase }) {
  return (
    <a href="#" className={`${className}`}>
      <span>{phrase}</span>
    </a>
  );
}

export default Logo;
