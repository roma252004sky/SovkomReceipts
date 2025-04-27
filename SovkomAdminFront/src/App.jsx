// App.jsx
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';  // Импортируем компонент Home
import Login from './pages/Login';  // Импортируем компонент Home
import Graph from './pages/Graph';  // Импортируем компонент Home
import './App.css';

function App() {
  return (
    <Routes>
      {/* Основной маршрут для главной страницы */}
      <Route path="/vinpin/front/" element={<Home />} />
      
      {/* Добавьте другие маршруты, если нужно */}
      <Route path="/vinpin/front/graph" element={<Graph />} />
    </Routes>
  );
}

export default App;
