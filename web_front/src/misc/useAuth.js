import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLogged, setIsLogged] = useState(false);
  const [profile, setProfile] = useState({
    name: '',
    surname: '',
    username: '',
    password: ''
  });

  const updateProfile = (updatedProfile) => {
    setProfile({ ...profile, ...updatedProfile });
  };

  return (
    <AuthContext.Provider value={{ isLogged, setIsLogged, profile, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
