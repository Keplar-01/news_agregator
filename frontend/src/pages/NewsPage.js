import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import NewsItem from '../components/news/NewsItem';

const NewsPage = () => {
  const [news, setNews] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    fetch(`http://localhost:8002/api/v1/news/${id}`)
      .then(response => response.json())
      .then(data => setNews(data));
  }, [id]);

  return (
    <div>
        {news && <NewsItem news={news} />}
    </div>
  );
};

export default NewsPage;