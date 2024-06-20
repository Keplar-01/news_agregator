import React, { useState } from 'react';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import './css/ModalAuth.css';

const ModalAuth = ({ isOpen, close }) => {
  const [formType, setFormType] = useState('login');

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={close}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="btn-group">
          <button className={`btn ${formType === 'login' ? 'btn-dark' : 'btn-light'}`} onClick={() => setFormType('login')}>Вход</button>
          <button className={`btn ${formType === 'register' ? 'btn-dark' : 'btn-light'}`} onClick={() => setFormType('register')}>Регистрация</button>
        </div>
        <div className="form-container">
          {formType === 'login' && <LoginForm onSuccess={close} />}
          {formType === 'register' && <RegisterForm />}
        </div>
        <button className="btn btn-light" onClick={close}>Закрыть</button>
      </div>
    </div>
  );
};

export default ModalAuth;