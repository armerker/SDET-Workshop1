#!/bin/bash
echo "🚀 Запуск всех тестов Banking UI..."

# Активируем venv если он есть
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
fi

# Запускаем основной скрипт
python run_all_tests.py