import React, { useState, useEffect } from 'react';
import { Modal, Button, notification } from 'antd';
import axios from 'axios';

// Функция для форматирования даты в формат dd.mm.yyyy
function formatDate(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы начинаются с 0, добавляем 1
  const year = date.getFullYear();
  return `${day}.${month}.${year}`;
}

const ActionModal = ({ id, onClose }) => {
  const [data, setData] = useState(null);  // Стейт для хранения данных

  useEffect(() => {
    // Загружаем данные при изменении id
    axios.get(`http://vinpin.ru/vinpin/main/getClientInfo?id=${id}`)
      .then((response) => {
        setData(response.data);  // Сохраняем данные в стейте
      })
      .catch((error) => {
        notification.error({
          message: 'Ошибка загрузки',
          description: error.message,
          placement: 'topRight',
        });
      });
  }, [id]);  // Перезапускаем запрос при изменении id

  // Функция для получения массива триггеров
  const getTriggers = () => {
    if (data && data.triggers) {
      // Разделяем строку на массив и удаляем лишние пробелы
      return data.triggers.split(',').map(trigger => trigger.trim());
    }
    return [];
  };

  // Проверка на наличие 'sms' в массиве триггеров
  const hasSmsTrigger = getTriggers().includes('sms');
  const hasEmailTrigger = getTriggers().includes('sms');

  return (
    <Modal
      title="Подробная информация"
      open={true}
      onCancel={onClose}
      footer={
        <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <div>
          <Button 
              style={{ 
                marginRight: 8, 
                backgroundColor: hasSmsTrigger ? 'green' : '#d32f2f', 
                borderColor: hasSmsTrigger ? 'green' : '#d32f2f' ,
                color: 'white'
              }}
              disabled={true} // Делаем кнопку некликабельной
            >
              {hasSmsTrigger ? 'СМС отправлено' : 'СМС не отправлено'}
            </Button>
            <Button 
            style={{ 
              marginRight: 8, 
              backgroundColor: hasSmsTrigger ? 'green' : '#d32f2f', 
              borderColor: hasSmsTrigger ? 'green' : '#d32f2f' ,
              color: 'white'
            }}
            disabled={true} // Делаем кнопку некликабельной
            >
              {hasSmsTrigger ? 'Email отправлено' : 'Email не отправлено'}
              </Button>
          </div>
          <Button key="close" onClick={onClose}>
            Закрыть
          </Button>
        </div>
      }
    >
      {/* Используем загруженные данные */}
      {data && (
        <>
          <p><strong>ФИО:</strong> {data.fio || 'Не указано'}</p>
          <p><strong>Телефон:</strong> {data.phone || 'Не указано'}</p>
          <p><strong>Компания:</strong> {data.enterprise || 'Не указано'}</p>
          {/* Форматируем дату, если она есть */}
          <p><strong>Дата начала сотрудничества:</strong> {data.dateStart ? formatDate(new Date(data.dateStart)) : 'Не указано'}</p>
          <p><strong>Примечание:</strong> {data.description || 'Не указано'}</p>
        </>
      )}
    </Modal>
  );
};

export default ActionModal;
