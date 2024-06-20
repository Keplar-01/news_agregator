import React, { useState } from 'react';
import './css/LoginForm.css';
import Cookies from 'js-cookie';

const LoginForm = ({ onSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameError, setUsernameError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Clear all error messages
    setUsernameError(null);
    setPasswordError(null);
    setError(null);

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('http://localhost:8002/api/v1/auth/login', {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });

    if (response.status === 422) {
      const data = await response.json();
      if (Array.isArray(data.detail)) {
        data.detail.forEach((error) => {
          if (error.loc.includes('username')) {
            setUsernameError('Требуется email');
          }
          if (error.loc.includes('password')) {
            setPasswordError('Требуется пароль');
          }
        });
      } else {
        setUsernameError('Неизвестная ошибка');
        setPasswordError('Неизвестная ошибка');
      }
    } else if (response.status === 401) {
      setError('Некорректный email или пароль');
    } else if (response.ok) {
      const data = await response.json();
      if (onSuccess) {
        onSuccess();
      }

      window.location.reload();
    }
  };

  return (
    <form className="d-flex flex-column" onSubmit={handleSubmit}>
      <label className="form-label">
        Логин:
        <input  name="email" className="form-control" value={username} onChange={e => setUsername(e.target.value)} />
        {usernameError && <div className="error-message">{usernameError}</div>}
      </label>
      <label className="form-label">
        Пароль:
        <input type="password" name="password" className="form-control" value={password} onChange={e => setPassword(e.target.value)} />
        {passwordError && <div className="error-message">{passwordError}</div>}
      </label>
      <input type="submit" value="Войти" className="btn btn-primary mt-3" />
       {error && <div className="error-message">{error}</div>}
    </form>
  );
};

export default LoginForm;