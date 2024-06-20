import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './DataSourceTable.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const DataSourcesTable = ({ dataSources, fetchDataSources }) => {
  const [editingId, setEditingId] = useState(null);
  const [editedDataSources, setEditedDataSources] = useState({});
  const navigate = useNavigate();

    const handleDelete = (id) => {
        const url = `http://localhost:8002/api/v1/parser/delete_parse_data/${id}`;
        const accessToken = Cookies.get('access_token');

        const headers = {
          'Accept': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        };

        axios.delete(url, { headers })
          .then(() => {
            toast.success('Данные успешно удалены');
            fetchDataSources();
          })
          .catch((error) => {
            if (error.response && error.response.status >= 400 && error.response.status < 500) {
              toast.error('У вас нет доступа к удалению');
            } else {
              toast.error('Неизвестная ошибка при удалении');
            }
            console.error('Error deleting data', error);
          });
  };

  const handleEdit = (dataSource) => {
    setEditingId(dataSource.id);
    setEditedDataSources({ ...dataSource });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedDataSources((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSave = (id) => {
    const url = `http://localhost:8002/api/v1/parser/update_parse_data/${id}`;
    const accessToken = Cookies.get('access_token');
    const headers = {
      'accept': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    };

    axios.put(url, editedDataSources, { headers })
      .then(() => {
        setEditingId(null);
        toast.success('Данные успешно обновлены');
        fetchDataSources();
      })
      .catch((error) => {
        if (error.response && error.response.status >= 400 && error.response.status < 500) {
          toast.error('У вас нет доступа к обнавлению');
          setTimeout(() => navigate('/'), 3000); // Redirect after 3 seconds
        } else {
          toast.error('Неизвестная ошибка');
        }
      });
  };

  const renderCell = (dataSource, field) => (
    editingId === dataSource.id ? (
      <input
        type="text"
        name={field}
        value={editedDataSources[field]}
        onChange={handleChange}
        className="form-control"
      />
    ) : (
      dataSource[field]
    )
  );

  return (
    <div>
      <table className="table">
        <thead>
          <tr>
            <th>Ссылка источника со списком новостей</th>
            <th>HTML-тег списка новостей</th>
            <th>HTML-атрибут списка новостей</th>
            <th>HTML-тег элемента новости</th>
            <th>Название HTML-атрибута элемента</th>
            <th>Значение HTML-атрибута элемента</th>
            <th>Тип URL</th>
            <th>К датасету</th>
            <th>Класс новости (Если к датасету)</th>
            <th>Название источника</th>
            <th className="hidden">ID</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {dataSources.map((dataSource) => (
            <tr key={dataSource.id}>
              <td>{renderCell(dataSource, 'url_list')}</td>
              <td>{renderCell(dataSource, 'html_tag_list')}</td>
              <td>{renderCell(dataSource, 'html_attr_list')}</td>
              <td>{renderCell(dataSource, 'html_tag_element')}</td>
              <td>{renderCell(dataSource, 'html_attr_element_type')}</td>
              <td>{renderCell(dataSource, 'html_attr_element_value')}</td>
              <td>{renderCell(dataSource, 'type_url')}</td>
              <td>{renderCell(dataSource, 'to_dataset')}</td>
              <td>{renderCell(dataSource, 'default_class_news')}</td>
              <td>{renderCell(dataSource, 'name')}</td>
              <td className="hidden">{dataSource.id}</td>
              <td>
                {editingId === dataSource.id ? (
                  <button
                    className="btn btn-outline-success"
                    onClick={() => handleSave(dataSource.id)}
                  >
                    Сохранить
                  </button>
                ) : (
                  <>
                    <button
                      className="btn btn-outline-info"
                      onClick={() => handleEdit(dataSource)}
                    >
                      Изменить
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(dataSource.id)}
                    >
                      Удалить
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataSourcesTable;
