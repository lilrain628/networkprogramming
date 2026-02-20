# Использование конкретной версии Ubuntu для обеспечения воспроизводимости
FROM ubuntu:22.04

# Метаданные
LABEL maintainer="Student <student@example.com>"
LABEL description="Учебный микросервис на FastAPI"

# Настройка переменных окружения для минимизации взаимодействия с установщиком пакетов
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновление индекса пакетов и установка необходимых системных зависимостей.
# Объединение команд в один слой RUN уменьшает итоговый размер образа.
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Создаем симлинк для python3 -> python (для удобства)
RUN ln -s /usr/bin/python3 /usr/bin/python

# Определение рабочей директории. Все последующие инструкции будут выполняться в ней.
WORKDIR /app

# Копирование файла зависимостей. Это делается до копирования основного кода,
# чтобы при изменении кода не переустанавливать библиотеки (использование кэша Docker).
COPY requirements.txt .

# Установка зависимостей Python. Флаг --no-cache-dir предотвращает хранение лишних файлов.
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование исходного кода микросервиса в контейнер.
COPY . .

# Создание непривилегированного пользователя для безопасности
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Переключение на непривилегированного пользователя
USER appuser

# Информирование Docker о порте, который приложение слушает внутри контейнера.
EXPOSE 8000

# Команда запуска приложения при старте контейнера.
# Использование exec-формы ["cmd", "arg1"] позволяет корректно передавать сигналы ОС процессу.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]