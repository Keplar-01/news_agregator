import React, { useEffect, useState } from 'react';

const ClassFilter = ({ onClassChange, onPositiveChange }) => {
  const [classes, setClasses] = useState([]);
  const [selectedClasses, setSelectedClasses] = useState([]);
  const [isPositive, setIsPositive] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8002/api/v1/news/classes')
      .then(response => response.json())
      .then(data => setClasses(data));
  }, []);

  const activeClasses = classes.filter(cls => cls.is_active);

  const handleClassChange = (classId) => {
    if (selectedClasses.includes(classId)) {
      setSelectedClasses(selectedClasses.filter(id => id !== classId));
    } else {
      setSelectedClasses([...selectedClasses, classId]);
    }
  };

  const handleReset = () => {
    setSelectedClasses([]);
    setIsPositive(false);
  };

  const handlePositiveChange = () => {
    setIsPositive(!isPositive);
  };

  useEffect(() => {
    onClassChange(selectedClasses);
    if (typeof onPositiveChange === 'function') {
      onPositiveChange(isPositive);
    }
  }, [selectedClasses, isPositive, onClassChange, onPositiveChange]);

  return (
    <div>
      {activeClasses.map(cls => (
        <button
           className="btn"
          key={cls.id}
          onClick={() => handleClassChange(cls.id)}
          style={{ backgroundColor: selectedClasses.includes(cls.id) ? 'lightgray' : 'white' }}
        >
          {cls.description}
        </button>
      ))}
      <button className="btn" style={{ backgroundColor:  isPositive? 'lightgray' : 'white' }} onClick={handlePositiveChange}>Без негатива</button>
      <button className="btn btn-dark" onClick={handleReset}>Сбросить</button>
    </div>
  );
};

export default ClassFilter;