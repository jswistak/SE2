import hero from "./resources/images/hero-plane.jpg";
import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  return (
    <div>
      <Header />
    </div>
  );
}

function Header(props) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const toggleElem = useRef(null);
  const navRef = useRef(null);
  const headerRef = useRef(null);
  const sectionRef = useRef(null);

  function toggleActive() {
    setIsActive(!isActive);
  }

  useEffect(() => {
    const toggleMenu = () => {
      setIsMenuOpen(!isMenuOpen);
    };
    const toggleElemCurrent = toggleElem.current;
    if (toggleElemCurrent) {
      toggleElemCurrent.addEventListener("click", toggleMenu);
      return () => {
        toggleElemCurrent.removeEventListener("click", toggleMenu);
      };
    }
  }, [toggleElem, isMenuOpen]);

  useEffect(() => {
    const header = headerRef.current;
    const nav = navRef.current;
    const toggleButton = toggleElem.current;
    const onScroll = () => {
      const isAtTop = window.scrollY === 0;
      if (nav != null && isAtTop) {
        nav.classList.toggle("active", false);
      }
      if (toggleButton != null && isAtTop) {
        toggleButton.classList.toggle("active", false);
      }
      if (header != null) {
        header.classList.toggle("sticky", !isAtTop);
      }
    };
    window.addEventListener("scroll", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
    };
  }, [headerRef]);

  return (
    <>
      <header className={isMenuOpen ? "sticky" : ""} ref={headerRef}>
        <img className="hero" src={hero} alt="" />
        <a href="#" className="logo">
          Roam!
        </a>
        <div
          className={`toggle ${isActive ? "active" : ""}`}
          ref={toggleElem}
          onClick={toggleActive}
        />
        <nav className={`${isActive ? "active" : ""}`} ref={navRef}>
          <ul>
            <li>
              <a href="#">Home</a>
            </li>
            <li>
              <a href="#">Profile</a>
            </li>
            <li>
              <a href="#">Team</a>
            </li>
            <li>
              <a href="#">Contact</a>
            </li>
          </ul>
        </nav>
      </header>
      <section ref={sectionRef}>
        <h2>Section's Header lorem ipsum</h2>
        <p>
          Nunc ac nisl sit amet nunc convallis fermentum in in diam. Donec
          sollicitudin risus leo, vitae aliquet tortor consectetur a. Ut nec
          lobortis tellus, et dignissim urna. Donec pellentesque volutpat urna,
          a aliquet leo. Donec vitae leo facilisis, varius arcu quis, laoreet
          eros. Morbi nunc urna, cursus vel enim venenatis, vestibulum auctor
          neque. Phasellus leo nisl, rutrum vitae sapien non, placerat ultrices
          tellus. Cras malesuada diam metus, aliquam dignissim massa suscipit
          eu. Duis vitae mi id neque tristique ullamcorper at quis nibh. Duis
          turpis massa, semper quis dolor quis, ultrices condimentum nibh.
          Quisque quis turpis sed metus consequat congue malesuada ac quam.
          Nulla tristique luctus laoreet. Pellentesque habitant morbi tristique
          senectus et netus et malesuada fames ac turpis egestas. Vestibulum
          ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia
          curae;
        </p>
        <p>
          Nunc ac nisl sit amet nunc convallis fermentum in in diam. Donec
          sollicitudin risus leo, vitae aliquet tortor consectetur a. Ut nec
          lobortis tellus, et dignissim urna. Donec pellentesque volutpat urna,
          a aliquet leo. Donec vitae leo facilisis, varius arcu quis, laoreet
          eros. Morbi nunc urna, cursus vel enim venenatis, vestibulum auctor
          neque. Phasellus leo nisl, rutrum vitae sapien non, placerat ultrices
          tellus. Cras malesuada diam metus, aliquam dignissim massa suscipit
          eu. Duis vitae mi id neque tristique ullamcorper at quis nibh. Duis
          turpis massa, semper quis dolor quis, ultrices condimentum nibh.
          Quisque quis turpis sed metus consequat congue malesuada ac quam.
          Nulla tristique luctus laoreet. Pellentesque habitant morbi tristique
          senectus et netus et malesuada fames ac turpis egestas. Vestibulum
          ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia
          curae;
        </p>
        <p>
          Nunc ac nisl sit amet nunc convallis fermentum in in diam. Donec
          sollicitudin risus leo, vitae aliquet tortor consectetur a. Ut nec
          lobortis tellus, et dignissim urna. Donec pellentesque volutpat urna,
          a aliquet leo. Donec vitae leo facilisis, varius arcu quis, laoreet
          eros. Morbi nunc urna, cursus vel enim venenatis, vestibulum auctor
          neque. Phasellus leo nisl, rutrum vitae sapien non, placerat ultrices
          tellus. Cras malesuada diam metus, aliquam dignissim massa suscipit
          eu. Duis vitae mi id neque tristique ullamcorper at quis nibh. Duis
          turpis massa, semper quis dolor quis, ultrices condimentum nibh.
          Quisque quis turpis sed metus consequat congue malesuada ac quam.
          Nulla tristique luctus laoreet. Pellentesque habitant morbi tristique
          senectus et netus et malesuada fames ac turpis egestas. Vestibulum
          ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia
          curae;
        </p>
      </section>
    </>
  );
}

export default App;
