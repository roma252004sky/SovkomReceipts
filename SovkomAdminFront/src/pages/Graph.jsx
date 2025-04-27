import React from 'react';
import { FaTable, FaChartBar } from 'react-icons/fa';  // Импорт иконок
import { Link } from 'react-router-dom';  // Для маршрутизации между страницами
import logo from '../../public/apple.png';  // Путь к логотипу

const Graph = () => {
  return (
    <div className="App">
      <div className="sidebar">
        <div className="sidebar-item">
          <Link to="/vinpin/front">
            <FaTable />
            <span>Таблица</span>
          </Link>
        </div>
        <div className="sidebar-item">
          <Link to="/vinpin/front/graph">
            <FaChartBar />
            <span>Dashboard</span>
          </Link>
        </div>
        
        {/* Логотип теперь внизу */}
        <div className="sidebar-footer">
          <img src={logo} alt="Logo" className="logo" />
        </div>
      </div>

      <div className="content">
        <h2>Dashboard</h2>
        <iframe 
            src="http://localhost:8080/d/aehahvgpf8bnkf/new-dashboard?orgId=1&&kiosk"
            width="100%"
            height="90%"
            frameborder="0"
            allowfullscreen>
        </iframe>
      </div>
    </div>
  );
};

export default Graph;
