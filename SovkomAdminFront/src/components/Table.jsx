import React, { useState, useEffect } from 'react';
import { Table, Button, Input, notification } from 'antd';
import ActionModal from './ActionModal';

const TableComponent = () => {
  const [data, setData] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [fioSearchText, setFioSearchText] = useState('');
  const [pageSize, setPageSize] = useState(10);

  const handlePageSizeChange = (value) => {
    setPageSize(value);  // Обновляем состояние pageSize
  };

  useEffect(() => {
    fetch('http://localhost:8080/sovkom/main/getClients')  // Заменить на реальный API
      .then((response) => {
        if (!response.ok) {
          throw new Error('Ошибка при загрузке данных');
        }
        return response.json();
      })
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        // Пример данных для использования, если API не доступен
        const r_data = [
          { userId: 1, scannedReceipts: 120, favoriteCategory: 'Продукты', monthlySum: 4500 },
          { userId: 2, scannedReceipts: 80, favoriteCategory: 'Одежда', monthlySum: 3200 },
          { userId: 3, scannedReceipts: 50, favoriteCategory: 'Техника', monthlySum: 2400 },
          { userId: 4, scannedReceipts: 200, favoriteCategory: 'Книги', monthlySum: 5300 },
          { userId: 5, scannedReceipts: 130, favoriteCategory: 'Еда', monthlySum: 4600 },
          { userId: 6, scannedReceipts: 90, favoriteCategory: 'Техника', monthlySum: 3800 },
          { userId: 7, scannedReceipts: 150, favoriteCategory: 'Одежда', monthlySum: 4900 },
          { userId: 8, scannedReceipts: 170, favoriteCategory: 'Книги', monthlySum: 5200 },
          { userId: 9, scannedReceipts: 110, favoriteCategory: 'Продукты', monthlySum: 4400 },
          { userId: 10, scannedReceipts: 80, favoriteCategory: 'Еда', monthlySum: 3500 },
          { userId: 11, scannedReceipts: 160, favoriteCategory: 'Техника', monthlySum: 4800 },
          { userId: 12, scannedReceipts: 140, favoriteCategory: 'Одежда', monthlySum: 5100 },
          { userId: 13, scannedReceipts: 180, favoriteCategory: 'Продукты', monthlySum: 4900 },
          { userId: 14, scannedReceipts: 100, favoriteCategory: 'Книги', monthlySum: 4600 },
          { userId: 15, scannedReceipts: 75, favoriteCategory: 'Еда', monthlySum: 3300 },
          { userId: 16, scannedReceipts: 130, favoriteCategory: 'Продукты', monthlySum: 4700 },
          { userId: 17, scannedReceipts: 60, favoriteCategory: 'Одежда', monthlySum: 2800 },
          { userId: 18, scannedReceipts: 190, favoriteCategory: 'Техника', monthlySum: 5100 },
          { userId: 19, scannedReceipts: 140, favoriteCategory: 'Книги', monthlySum: 5000 },
          { userId: 20, scannedReceipts: 110, favoriteCategory: 'Еда', monthlySum: 4200 }
          // Здесь можно добавить другие данные
        ];
        setData(r_data);

        notification.error({
          message: 'Ошибка загрузки',
          description: error.message,
          placement: 'topRight',
        });
      });
  }, []);

  const handleOpenModal = (row) => {
    setSelectedRow(row);
  };

  const handleCloseModal = () => {
    setSelectedRow(null);
  };

  const handleFioSearchChange = (e) => {
    setFioSearchText(e.target.value);
  };

  // Фильтрация данных
  const filteredData = data.filter((item) => {
    const matchesFio = item.userId.toString().includes(fioSearchText.toLowerCase());
    return matchesFio;
  });

  const columns = [
    { title: 'User ID', dataIndex: 'userId', key: 'userId', sorter: (a, b) => a.userId - b.userId, align: 'center' },
    { title: 'Количество отсканированных чеков', dataIndex: 'scannedReceipts', key: 'scannedReceipts', align: 'center' },
    { title: 'Любимая категория', dataIndex: 'favoriteCategory', key: 'favoriteCategory' },
    { title: 'Сумма за месяц', dataIndex: 'monthlySum', key: 'monthlySum', sorter: (a, b) => b.monthlySum - a.monthlySum, align: 'center' },
    // {
    //   title: 'Действия',
    //   key: 'actions',
    //   align: 'center',
    //   render: (_, record) => (
    //     <div className="centered-button">
    //       <Button type="primary" onClick={() => handleOpenModal(record)}>
    //         Подробнее
    //       </Button>
    //     </div>
    //   ),
    // },
  ];

  return (
    <div className="table-container">
      <Table
        columns={columns}
        dataSource={filteredData}  // Отображаем отфильтрованные данные
        rowKey="userId"
        pagination={{
          pageSize: pageSize,  // Устанавливаем количество записей на странице из состояния
          showSizeChanger: true,  // Показываем возможность выбора количества записей
          pageSizeOptions: ['5', '10', '20', '50'],  // Доступные варианты для выбора количества записей на странице
          onShowSizeChange: (current, size) => setPageSize(size),  // Обработчик изменения количества записей
        }}
        bordered
        rowClassName="centered-row"
      />
      {selectedRow && <ActionModal id={selectedRow.userId} onClose={handleCloseModal} />}
    </div>
  );
};

export default TableComponent;
