import React, { useState } from 'react';
import './css/RegisterForm.css';

const RegisterForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [errorMessage, setErrorMessage] = useState(''); // Add this line

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Create a new object
    const data = {
      username: username,
      password: password,
      name: name
    };

    const response = await fetch('http://localhost:8002/api/v1/auth/registration', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data), // Send the JSON data
      credentials: 'include' // This is required to include the cookies in the response
    });

    if (response.ok) {
      // Reload the page
      window.location.reload();
    } else {
      const data = await response.json();
      setErrorMessage(data.detail); // Add this line
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="register-container">
        <div className="register-form-group">
          <label className="form-label">
            Имя:
            <input type="text" name="name" className="form-control" value={name} onChange={e => setName(e.target.value)} />
          </label>
          <label className="form-label">
            Логин:
            <input  name="email" className="form-control" value={username} onChange={e => setUsername(e.target.value)} />
          </label>
        </div>
        <label className="register-form-label form-label">
          Пароль:
          <input type="password" name="password" className="form-control" value={password} onChange={e => setPassword(e.target.value)} />
        </label>
        <div className="d-flex justify-content-center">
          <input className="register-form-submit btn btn-primary w-100" type="submit" value="Зарегистрироваться" /> {/* Add w-100 class */}
        </div>
        {errorMessage && <div className="error-message">{errorMessage}</div>} {/* Add this line */}
      </div>
    </form>
  );
}

export default RegisterForm;