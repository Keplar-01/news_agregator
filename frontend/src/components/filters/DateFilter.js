import React from 'react';
import './DateFilter.css'
const DateFilter = ({ dateFrom, dateTo, onChange }) => {
  const handleDateFromChange = (event) => {
    onChange({ dateFrom: event.target.value, dateTo });
  };

  const handleDateToChange = (event) => {
    onChange({ dateFrom, dateTo: event.target.value });
  };

  return (
    <div className="form-group">
      <label>
        От:
        <input type="date" value={dateFrom} onChange={handleDateFromChange} className="form-control" />
      </label>
      <label>
        До:
        <input type="date" value={dateTo} onChange={handleDateToChange} className="form-control" />
      </label>
    </div>
  );
};

export default DateFilter;