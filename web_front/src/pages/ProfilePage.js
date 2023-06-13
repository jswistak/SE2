import React, { useState, useEffect } from 'react';
import { useAuth } from '../misc/useAuth';
import Header from '../components/Header';
import './ProfilePage.css'
import { callApi } from '../misc/Api';

const ProfilePage = () => {
  const { profile, updateProfile } = useAuth();
  const [username, setUsername] = useState(profile.username);
  const [email, setEmail] = useState(profile.email);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch the list of users from the API
    const fetchUsers = async () => {
      try {
        const response = callApi("users/").then((data)=>setUsers(data));
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);

  const handleProfileUpdate = async (e) => {
    e.preventDefault();

    // Find the current user in the users list
    const currentUser = users.find((user) => user.username === profile.username);
    console.log(currentUser);
    if (currentUser) {
      const updatedUser = { ...currentUser, username, email };
      console.log(updatedUser);
      try {
        // Update the user profile with PUT request
        const response = await fetch(currentUser.url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatedUser),
        });

        if (response.ok) {
          // Update the profile context with the new username and email
          if (username) {
            updateProfile({ username });
          }
          if (email) {
            updateProfile({ email });
          }
          alert('Profile updated successfully!');
        } else {
          alert('Failed to update profile. Please try again.');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
        alert('Failed to update profile. Please try again.');
      }
    } else {
      alert('Current user not found in the users list.');
    }
  };

  return (
    <div className="profile-container">
      <Header sticky={true} />
      <h1>Profile Management</h1>
      <div>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <hr />
      <button type="button" onClick={handleProfileUpdate}>
        Update Profile
      </button>
    </div>
  );
};

export default ProfilePage;

