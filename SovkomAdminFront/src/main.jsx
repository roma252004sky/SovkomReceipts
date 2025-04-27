// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';  // Импортируем новый API для React 18
import { BrowserRouter as Router } from 'react-router-dom';  // Импортируем Router для маршрутизации
import './index.css';  // Импортируем ваши стили
import 'antd/dist/reset.css';  // Импортируем стили Ant Design
import App from './App';  // Импортируем компонент App

// Используем новый метод createRoot
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <App />  {/* Оборачиваем App в Router */}
    </Router>
  </React.StrictMode>
);
