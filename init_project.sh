#!/bin/sh
set -e

echo "==> Сборка образов для контейнеров"
docker compose build

echo "==> Запуск PostgreSQL и Redis..."
docker compose up -d

echo "==> Ожидание готовности PostgreSQL..."
sleep 10

echo "==> Инициализация базы данных Redash..."
docker compose run --rm redash create_db

echo "==> Запуск всех сервисов..."
docker compose up -d

echo "==> Готово. Redash должен быть доступен на http://localhost:5000"
echo "==> Для остановки пропишите docker compose down"