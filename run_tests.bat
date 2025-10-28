@echo off
echo 🚀 Запуск всех тестов Banking UI...

REM Активируем venv если он есть
if exist ".venv" (
    call .venv\Scripts\activate
)

REM Запускаем основной скрипт
python run_all_tests.py

pause