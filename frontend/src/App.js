import React from 'react';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import NewsList from './pages/NewsList';
import NewsPage from './pages/NewsPage';
import UserProfile from './pages/Profile';
import NewsToCheckPage from './pages/NewsToCheckPage';
import Header from './components/Header';
import './App.css';
import DataSourcePage from "./pages/DataSourcePage"; // Импорт App.css
import scheduleRefreshToken from "./utils/refresh";

const App = () => {
    scheduleRefreshToken();
    return (
        <Router>
            <Header/>
            <div className="app-content">
                <Routes>
                    <Route path="/" element={<NewsList/>}/>
                    <Route path="/news/:id" element={<NewsPage/>}/>
                    <Route path="/parse_data" element={<DataSourcePage/>}/>
                    <Route path="/markup" element={<NewsToCheckPage/>}/>
                    <Route path="/profile" element={<UserProfile/>}/>
                </Routes>
            </div>
        </Router>
    );
};

export default App;