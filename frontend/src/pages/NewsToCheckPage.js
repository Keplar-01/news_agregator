import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NewsToCheckPage = () => {
  const [news, setNews] = useState(null);
  const [classes, setClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // Add loading state
const handleDownload = () => {
    axios.get('http://localhost:8002/api/v1/news/train_news', { responseType: 'blob' })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'dataset.csv'); // or any other filename
        document.body.appendChild(link);
        link.click();
      });
  };
  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = () => {
    setIsLoading(true); // Set loading state to true when fetching starts
    axios.get('http://localhost:8002/api/v1/news/train_one?date_to=2024-06-02T16%3A49%3A29.663549&classes=1')
      .then(response => {
        setNews(response.data);
        setSelectedClass(response.data.classes_id.toString());
      })
      .finally(() => setIsLoading(false)); // Set loading state to false when fetching ends

    axios.get('http://localhost:8002/api/v1/news/classes')
      .then(response => {
        setClasses(response.data);
      });
  };

  const handleClassChange = (event) => {
    setSelectedClass(event.target.value);
  };

  const handleSave = () => {
    setIsLoading(true); // Set loading state to true when saving starts
    axios.put(`http://localhost:8002/api/v1/news/train/${news.id}?classes_id=${selectedClass}`)
      .then(response => {
        fetchNews();
      })
      .finally(() => setIsLoading(false)); // Set loading state to false when saving ends
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container">
      {news && (
        <div className="row">
          <div className="col-md-8">
            <h1>{news.title}</h1>
            <p>{news.text}</p>
            <a href={news.url}>Источник: {news.name_source}</a>
          </div>
          <div className="col-md-4">
            <p>Класс: {news.classes_names}</p>
            <select className="form-select" value={selectedClass} onChange={handleClassChange} disabled={isLoading}>
              <option value="-">-</option>
              {classes.map(cls => (
                <option key={cls.id} value={cls.id.toString()}>{cls.description}</option>
              ))}
            </select>
            <button className="btn btn-primary mt-2" onClick={handleSave} disabled={isLoading}>Сохранить</button>
            <button className="btn mt-2" onClick={handleDownload} disabled={isLoading}>Скачать датасет</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewsToCheckPage;