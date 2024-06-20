import React, { useEffect, useState } from 'react';
import NewsListItem from '../components/news/NewsListItem';
import DateFilter from '../components/filters/DateFilter';
import ClassFilter from '../components/filters/ClassFilter';
import './NewsList.css';

const NewsList = () => {
  const [news, setNews] = useState([]);
  const [limit, setLimit] = useState(25);
  const [offset, setOffset] = useState(0);
  const [dateFrom, setDateFrom] = useState(null);
  const [dateTo, setDateTo] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isPositive, setIsPositive] = useState(false);

  const handleDateChange = ({ dateFrom, dateTo }) => {
    setDateFrom(dateFrom);
    setDateTo(dateTo);
  };

  const handleNextPage = () => {
    setOffset(offset + limit);
  };

  const handlePrevPage = () => {
    setOffset(Math.max(0, offset - limit));
  };

  const handlePositiveChange = (positive) => {
    setIsPositive(positive);
  };

  const [selectedClasses, setSelectedClasses] = useState([]);

  const handleClassChange = (classIds) => {
    setSelectedClasses(classIds);
  };

  useEffect(() => {
    let url = `http://localhost:8002/api/v1/news?limit=${limit}&offset=${offset}`;

    if (dateFrom) {
      url += `&date_from=${dateFrom}`;
    }

    if (dateTo) {
      url += `&date_to=${dateTo}`;
    }

    if (selectedClasses.length > 0) {
      url += `&classes=${selectedClasses.join(',')}`;
    }
    if (isPositive) {
      url += `&is_positive=true`;
    }

    fetch(url)
      .then(response => response.json())
      .then(data => setNews(data));
  }, [limit, offset, dateFrom, dateTo, selectedClasses, isPositive]);

  return (
    <div>
      <div className="filter-data">
        <DateFilter dateFrom={dateFrom} dateTo={dateTo} onChange={handleDateChange} />
        <ClassFilter onClassChange={handleClassChange} onPositiveChange={handlePositiveChange} />
      </div>
      {news.map(item => (
        <NewsListItem key={item.id} news={item} />
      ))}
      <button onClick={handlePrevPage}>Previous Page</button>
      <button onClick={handleNextPage}>Next Page</button>
    </div>
  );
};

export default NewsList;