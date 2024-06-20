import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { toast } from 'react-toastify';

const AddDataSourceForm = ({ onClose, onDataSourceAdded }) => {
  const [newDataSource, setNewDataSource] = useState({
    url_list: '',
    html_tag_list: '',
    html_attr_list: '',
    html_tag_element: '',
    html_attr_element_type: '',
    html_attr_element_value: '',
    type_url: 'rss',
    to_dataset: true,
    default_class_news: '',
    name: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewDataSource((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const accessToken = Cookies.get('access_token'); // Получаем access token из куков
    const headers = {
      'accept': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    };

    axios.post('http://localhost:8002/api/v1/parser/add_parse_data', newDataSource, { headers })
      .then(() => {
        toast.success('Источник данных успешно добавлен');
        onDataSourceAdded();
        onClose();
      })
      .catch((error) => {
        if (error.response && error.response.status >= 400 && error.response.status < 500) {
          toast.error('У вас нет доступа для создания источника данных');
        } else {
          toast.error('Произошла непредвиденная ошибка при создании источника данных');
        }
      });
  };

  return (
    <div className="popup">
      <div className="popup-inner">
        <h2>Добавить новый источник данных</h2>
        <form onSubmit={handleSubmit}>

          <div className="row">
            <div className="col-sm-6">
              <div className="form-group">
                <label>Ссылка источника со списком новостей</label>
                <input
                  type="text"
                  className="form-control"
                  name="url_list"
                  value={newDataSource.url_list}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>HTML-тег списка новостей</label>
                <input
                  type="text"
                  className="form-control"
                  name="html_tag_list"
                  value={newDataSource.html_tag_list}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>HTML-атрибут списка новостей</label>
                <input
                  type="text"
                  className="form-control"
                  name="html_attr_list"
                  value={newDataSource.html_attr_list}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>HTML-тег элемента новости</label>
                <input
                  type="text"
                  className="form-control"
                  name="html_tag_element"
                  value={newDataSource.html_tag_element}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="col-sm-6">
              <div className="form-group">
                <label>Название HTML-атрибута элемента</label>
                <input
                  type="text"
                  className="form-control"
                  name="html_attr_element_type"
                  value={newDataSource.html_attr_element_type}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Значение HTML-атрибута элемента</label>
                <input
                  type="text"
                  className="form-control"
                  name="html_attr_element_value"
                  value={newDataSource.html_attr_element_value}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Тип URL</label>
                <select
                  className="form-control"
                  name="type_url"
                  value={newDataSource.type_url}
                  onChange={handleChange}
                >
                  <option value="rss">RSS</option>
                  <option value="html">HTML</option>
                  <option value="xml">XML</option>
                </select>
              </div>

              <div className="form-group">
                <label>К датасету</label>
                <select
                  className="form-control"
                  name="to_dataset"
                  value={newDataSource.to_dataset}
                  onChange={handleChange}
                >
                  <option value={true}>Да</option>
                  <option value={false}>Нет</option>
                </select>
              </div>

              <div className="form-group">
                <label>Класс новости (Если к датасету)</label>
                <input
                  type="text"
                  className="form-control"
                  name="default_class_news"
                  value={newDataSource.default_class_news}
                  onChange={handleChange}
                />
              </div>

              <div className="form-group">
                <label>Название источника</label>
                <input
                  type="text"
                  className="form-control"
                  name="name"
                  value={newDataSource.name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          </div>

          <div className="form-group">
            <button type="submit" className="btn btn-primary mr-2">
              Создать
            </button>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddDataSourceForm;
