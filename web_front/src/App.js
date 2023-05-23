import React, { createContext } from 'react';
import { Routes, Route } from 'react-router-dom';

import useIsMobile from './misc/useIsMobile';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';


export const IsMobileContext = createContext();


function App() {

  const isMobile = useIsMobile();

  return (
    <IsMobileContext.Provider value={isMobile}>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/Login" element={<LoginPage currentForm='login' />} />
        <Route path="/Profile" element={<ProfilePage />} />
      </Routes>
    </IsMobileContext.Provider>
  );
}

export default App;
