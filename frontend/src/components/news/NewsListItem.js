import React from 'react';// Импорт стилей Bootstrap
import './NewsItem.css';
import {Link} from "react-router-dom"; // Импорт пользовательских стилей
import {formatDate} from "../../utils";
const NewsListItem = ({ news }) => (
  <div className="news-item">
    <h2>{news.title}</h2>
    <p className="text-muted">Жанр: {news.classes_names}</p>
    <p className="text-muted"> Дата: {formatDate(news.date)} </p>
   <Link to={`/news/${news.id}`} className="btn btn-primary mr-2">
      Прочитать новость
    </Link>
      <a href={news.url} className="btn btn-secondary">Перейти на источник новости</a>
  </div>
);
export default NewsListItem;