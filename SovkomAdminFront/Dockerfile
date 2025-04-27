# Этап сборки (Build stage)
FROM node:22 AS build
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
# Копируем package.json и package-lock.json (если есть)
COPY package*.json ./
# Устанавливаем все зависимости
RUN npm install
# Копируем весь исходный код проекта в контейнер
COPY . .
# Строим проект
RUN npm run build
# Этап для продакшн (Production stage)
FROM node:22
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
# Копируем только собранные файлы (из build-деректории)
COPY --from=build /app/dist /app/dist 
# Копируем package.json и package-lock.json
COPY package*.json ./
# Устанавливаем только необходимые зависимости для продакшн
RUN npm install --production
# Открываем порт для приложения
EXPOSE 5173
# Запускаем сервер
CMD ["npx", "serve", "-s", "dist", "-l", "5173"]
