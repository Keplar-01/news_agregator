import React, { useEffect, useState } from "react";
import DataSourcesTable from "../components/DataSourceTable";
import AddDataSourceForm from "../components/AddDataSourceForm";
import axios from 'axios';
import Cookies from 'js-cookie';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import "../components/AddDataSourceForm.css";
import 'bootstrap/dist/css/bootstrap.min.css';

const DataSourcePage = () => {
  const [dataSources, setDataSources] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false); // Состояние для отображения попапа
  const navigate = useNavigate();

  const fetchDataSources = () => {
    const accessToken = Cookies.get('access_token'); // Получаем access token из куков
    const headers = {
      'accept': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    };

    axios.get('http://localhost:8002/api/v1/parser/parse_data', { headers })
      .then(response => {
        setDataSources(response.data);
      })
      .catch(error => {
        if (error.response && error.response.status >= 400 && error.response.status < 500) {
          toast.error('Произошла ошибка. Перенаправление на главную страницу.');
          setTimeout(() => navigate('/'), 3000); // Редирект через 3 секунды
        } else {
          toast.error('Произошла непредвиденная ошибка.');
        }
      });
  };

  useEffect(() => {
    fetchDataSources();
  }, []);

  const handleAddButtonClick = () => {
    setShowAddForm(true);
  };

  const handleCloseForm = () => {
    setShowAddForm(false);
  };

  return (
    <div>
      <ToastContainer />
      <DataSourcesTable dataSources={dataSources} fetchDataSources={fetchDataSources} />
      <button className="btn btn-primary mt-3" onClick={handleAddButtonClick}>
        Добавить новый источник
      </button>
      {showAddForm && (
        <AddDataSourceForm onClose={handleCloseForm} onDataSourceAdded={fetchDataSources} />
      )}
    </div>
  );
};

export default DataSourcePage;
