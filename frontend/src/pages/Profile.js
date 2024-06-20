import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [userClasses, setUserClasses] = useState([]);
  const [availableClasses, setAvailableClasses] = useState([]);
  const [selectedClassIds, setSelectedClassIds] = useState([]);
  const [parseDataSources, setParseDataSources] = useState([]);
  const [selectedParseDataIds, setSelectedParseDataIds] = useState([]);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const accessToken = Cookies.get('access_token');
        const headers = {
          'accept': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        };

        const userProfileResponse = await axios.get('http://localhost:8002/api/v1/user/me/', { headers });
        setUser(userProfileResponse.data);

        const userClassesResponse = await axios.get('http://localhost:8002/api/v1/user/classes/', { headers });
        setUserClasses(userClassesResponse.data.map(cls => cls.id));

        const availableClassesResponse = await axios.get('http://localhost:8002/api/v1/news/classes', { headers });
        setAvailableClasses(availableClassesResponse.data.filter(cls => cls.is_active));

        const parseDataResponse = await axios.get('http://localhost:8002/api/v1/parser/parse_data', { headers });
        setParseDataSources(parseDataResponse.data);

        setSelectedClassIds(userClassesResponse.data.map(cls => cls.id));
        setSelectedParseDataIds(parseDataResponse.data.map(pd => pd.id));
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    };

    fetchUserProfile();
  }, []);

  const handleClassToggle = (classId) => {
    const isSelected = selectedClassIds.includes(classId);
    if (isSelected) {
      setSelectedClassIds(selectedClassIds.filter(id => id !== classId));
    } else {
      setSelectedClassIds([...selectedClassIds, classId]);
    }
  };

  const handleParseDataToggle = (parseDataId) => {
    const isSelected = selectedParseDataIds.includes(parseDataId);
    if (isSelected) {
      setSelectedParseDataIds(selectedParseDataIds.filter(id => id !== parseDataId));
    } else {
      setSelectedParseDataIds([...selectedParseDataIds, parseDataId]);
    }
  };

  const handleSaveClasses = async () => {
    try {
      const accessToken = Cookies.get('access_token');
      const headers = {
        'accept': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      };

      await axios.post('http://localhost:8002/api/v1/user/attach_classes/', selectedClassIds, { headers });

      const userClassesResponse = await axios.get('http://localhost:8002/api/v1/user/classes/', { headers });
      setUserClasses(userClassesResponse.data.map(cls => cls.id));

    } catch (error) {
      console.error('Error saving classes:', error);
    }
  };

  const handleSaveParseData = async () => {
    try {
      const accessToken = Cookies.get('access_token');
      const headers = {
        'accept': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      };

      await axios.post('http://localhost:8002/api/v1/user/attach_parse_data/', selectedParseDataIds, { headers });

      const parseDataResponse = await axios.get('http://localhost:8002/api/v1/parser/parse_data', { headers });
      setParseDataSources(parseDataResponse.data);

    } catch (error) {
      console.error('Error saving parse data sources:', error);
    }
  };

  return (
    <div className="container mt-5">
      <h2>Личный кабинет пользователя</h2>
      {user && (
        <div className="card mb-3">
          <div className="card-body">
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Имя:</strong> {user.name}</p>
            <p><strong>Роль:</strong> {user.role}</p>
            <p><strong>ID:</strong> {user.id}</p>
            <p><strong>Дата создания:</strong> {new Date(user.created_at).toLocaleDateString()}</p>
          </div>
        </div>
      )}

      <div className="row">
        <div className="col-md-6">
          <div className="card mb-3">
            <div className="card-body">
              <h3 className="card-title">Доступные классы новостей</h3>
              <ul className="list-group">
                {availableClasses.map(cls => (
                  <li key={cls.id} className="list-group-item">
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        value={cls.id}
                        id={`class${cls.id}`}
                        checked={selectedClassIds.includes(cls.id)}
                        onChange={() => handleClassToggle(cls.id)}
                      />
                      <label className="form-check-label" htmlFor={`class${cls.id}`}>
                        {cls.name} - {cls.description}
                      </label>
                    </div>
                  </li>
                ))}
              </ul>
              <button className="btn btn-primary mt-3" onClick={handleSaveClasses}>Сохранить выбранные классы</button>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card mb-3">
            <div className="card-body">
              <h3 className="card-title">Источники данных</h3>
              <ul className="list-group">
                {parseDataSources.map(pd => (
                  <li key={pd.id} className="list-group-item">
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        value={pd.id}
                        id={`parseData${pd.id}`}
                        checked={selectedParseDataIds.includes(pd.id)}
                        onChange={() => handleParseDataToggle(pd.id)}
                      />
                      <label className="form-check-label" htmlFor={`parseData${pd.id}`}>
                        {pd.name}
                      </label>
                    </div>
                  </li>
                ))}
              </ul>
              <button className="btn btn-primary mt-3" onClick={handleSaveParseData}>Сохранить выбранные источники</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
