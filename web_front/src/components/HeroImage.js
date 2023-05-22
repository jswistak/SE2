import React from "react";

function HeroImage({ className, src }) {
  return <img className={`${className}`} src={src} alt="" />;
}

export default HeroImage;