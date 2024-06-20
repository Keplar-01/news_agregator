import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import Modal from './auth/ModalAuth';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Header.css';
import Cookies from 'js-cookie';

// Стратегии для разных ролей пользователя
const strategies = {
  default: [''],
  checker: ['', 'markup'],
  admin: ['', 'markup', 'parse_data']
};

const Header = () => {
  const [isModalOpen, setModalOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [navigationLinks, setNavigationLinks] = useState([]);

  const openModal = () => {
    setModalOpen(true);
  };

  const closeModal = () => setModalOpen(false);

  const handleLogout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    window.location.reload();
  };

  // Функция для выбора стратегии в зависимости от роли пользователя
  const selectStrategy = (role) => {
    return strategies[role] || strategies.default;
  };

  useEffect(() => {
    const fetchUser = async () => {
      const accessToken = Cookies.get('access_token');

      if (!accessToken) {
        setNavigationLinks(strategies.default);
        return;
      }

      fetch('http://localhost:8002/api/v1/user/me/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }).then(async (response) => {
        if (response.status === 401) {
          Cookies.remove('access_token');
          setUser(null);

        } else if (response.ok) {
          const data = await response.json();
          setUser(data);
          setNavigationLinks(selectStrategy(data.role));
        }
      });
    };

    fetchUser();
  }, []);

  return (
    <header className="header">
      <div className="header-content">
        <h1 className="app-name">NEWS_TAGER</h1>

        <nav className="nav-links">
          {navigationLinks.map(link => (
            <NavLink key={link} to={`/${link}`} className="nav-link" activeClassName="active-link">
              {link === '' ? 'Новости' : link === 'markup' ? 'Разметка' : 'Источники данных'}
            </NavLink>
          ))}
        </nav>

        <div className="user-controls">
          {user ? (
            <div className="btn-group">
              <NavLink to="/profile" className="btn btn-light">Пользователь: {user.name}</NavLink>
              <button onClick={handleLogout} className="btn btn-dark">Выход</button>
            </div>
          ) : (
            <button onClick={openModal} className="nav-link">Вход/Регистрация</button>
          )}
        </div>
      </div>
      <Modal isOpen={isModalOpen} close={closeModal} />
    </header>
  );
};

export default Header;
