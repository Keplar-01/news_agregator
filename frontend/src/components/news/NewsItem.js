import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Импорт стилей Bootstrap
import './NewsItem.css';
import {Link} from "react-router-dom"; // Импорт пользовательских стилей

const NewsItem = ({news}) => (
    <div className="news-item" id={news.id}>
        <h2>{news.title}</h2>
        <p className="text-muted">Дата публикации: {news.date}</p>
        <p className="text-muted">Жанр: {news.classes}</p>
        <p className="content">{news.text}</p>
        <a href={news.url} className="btn btn-secondary">{news.name_source}</a>
        <Link to={`/`} className="btn btn-primary">Вернуться к списку новостей</Link>
    </div>
);
export default NewsItem;