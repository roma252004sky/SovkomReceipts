import React, { useState } from 'react';
import { Button, Input, Form, notification } from 'antd';
import logo from '../../public/vinpin-white-logo.svg';  // Путь к логотипу
import axios from 'axios';
import "../assets/css/Login.css"

const Login = () => {
  const [loading, setLoading] = useState(false);

  // Обработчик отправки формы
  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      // Отправка POST запроса на сервер
      const response = await axios.post('https://your-api-endpoint.com/login', {
        username: values.username,
        password: values.password,
      });

      // Если запрос успешен
      notification.success({
        message: 'Успешный вход',
        description: 'Вы успешно вошли в систему!',
      });

      // Здесь вы можете обработать успешный вход, например, сохранить токен
      console.log(response.data);
    } catch (error) {
      // Если запрос не удался
      notification.error({
        message: 'Ошибка',
        description: 'Не удалось войти в систему. Проверьте ваши данные.',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="container">
        <div className="header">
          <img src={logo} alt="Logo" className="logo" />
        </div>
        <div className="login-container">
          <h2>Вход в систему</h2>
          <Form onFinish={handleSubmit}>
            <Form.Item
              name="username"
              rules={[{ required: true, message: 'Пожалуйста, введите ваш логин!' }]}
            >
              <Input
                placeholder="Логин"
                size="large"
                autoComplete="off"
              />
            </Form.Item>

            <Form.Item
              name="password"
              rules={[{ required: true, message: 'Пожалуйста, введите ваш пароль!' }]}
            >
              <Input.Password
                placeholder="Пароль"
                size="large"
                autoComplete="off"
              />
            </Form.Item>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                block
                loading={loading}
                size="large"
              >
                Войти
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default Login;

