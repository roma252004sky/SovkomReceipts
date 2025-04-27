# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libgl1-mesa-glx \
    libzbar-dev \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chrome и ChromeDriver (оставляем оригинальную логику)
RUN CHROME_VERSION=$(curl -sSL https://googlechromelabs.github.io/chrome-for-testing/ | awk -F 'Version:' '/Stable/ {print $2}' | awk '{print $1}' | sed 's/<code>//g; s/<\/code>//g') \
    && CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip" \
    && CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
    && curl -sSL ${CHROME_URL} -o /tmp/chrome.zip \
    && curl -sSL ${CHROMEDRIVER_URL} -o /tmp/chromedriver.zip \
    && unzip /tmp/chrome.zip -d /opt \
    && unzip /tmp/chromedriver.zip -d /opt \
    && mv /opt/chrome-linux64 /opt/google \
    && mv /opt/chromedriver-linux64 /opt/google/chromedriver \
    && ln -s /opt/google/chrome /usr/bin/google-chrome \
    && ln -s /opt/google/chromedriver/chromedriver /usr/local/bin/ \
    && rm -rf /tmp/*.zip

# Настраиваем рабочее окружение
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Настраиваем непривилегированного пользователя
# КЭШ-ДИРЕКТОРИИ
RUN useradd -m appuser \
    # Даем права на системные директории только для конкретных путей
    && mkdir -p /usr/local/lib/python3.10/site-packages/qrdet/.model \
    && chown -R appuser:appuser /usr/local/lib/python3.10/site-packages/qrdet \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /home/appuser

# Переключаемся на непривилегированного пользователя
USER appuser

# Устанавливаем переменные окружения для путей к кэшу
ENV PYTHONUNBUFFERED=1 \
    ULTRAlytics_HOME=/home/appuser/.cache/ultralytics \
    QRDET_CACHE_DIR=/home/appuser/.cache/qrdet \
    TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface

# Запуск приложения
CMD ["python", "app.py"]