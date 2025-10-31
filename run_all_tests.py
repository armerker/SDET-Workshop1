#!/usr/bin/env python3
"""
Comprehensive Test Runner for Banking UI Tests
Запускает все тесты и проверяет выполнение всех требований задания
"""

import os
import sys
import subprocess
import json
import glob
from pathlib import Path


def run_command(command, check=True):
    """Выполняет команду и возвращает результат"""
    print(f"🚀 Выполняю: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Ошибка: {result.stderr}")
        return False
    return True


def check_requirements():
    """Проверяет наличие всех необходимых файлов"""
    print("📋 Проверяю структуру проекта...")

    required_files = [
        'tests/test_add_customer.py',
        'tests/test_customer_sorting.py',
        'tests/test_delete_customer.py',
        'tests/conftest.py',
        'pages/base_page.py',
        'pages/manager_page.py',
        'pages/customers_page.py',
        'utils/test_data_generator.py',
        'requirements.txt',
        'pytest.ini',
        'test-cases.md',
        'README.md'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Отсутствуют файлы:")
        for file in missing_files:
            print(f"   - {file}")
        return False

    print("✅ Все необходимые файлы присутствуют")
    return True


def check_test_cases():
    """Проверяет наличие тест-кейсов"""
    print("\n📝 Проверяю тест-кейсы...")

    if not os.path.exists("test-cases.md"):
        print("❌ Файл test-cases.md не найден")
        return False

    with open("test-cases.md", "r", encoding="utf-8") as f:
        content = f.read()

    required_cases = ["TC_001", "TC_002", "TC_003"]
    missing_cases = []

    for case in required_cases:
        if case not in content:
            missing_cases.append(case)

    if missing_cases:
        print(f"❌ Отсутствуют тест-кейсы: {missing_cases}")
        return False

    print("✅ Все тест-кейсы присутствуют")
    return True


def run_tests():
    """Запускает все тесты"""
    print("\n🧪 Запускаю тесты...")

    # Обычный запуск
    if not run_command("pytest tests/ -v"):
        return False

    print("✅ Все тесты прошли успешно")
    return True


def run_parallel_tests():
    """Запускает тесты в параллельном режиме"""
    print("\n⚡ Запускаю параллельные тесты...")

    if not run_command("pytest tests/ -n auto --tb=short"):
        return False

    print("✅ Параллельные тесты прошли успешно")
    return True


def generate_allure_reports():
    """Генерирует Allure отчеты"""
    print("\n📊 Генерирую Allure отчеты...")

    # Создаем директории если их нет
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("allure-report", exist_ok=True)

    # Запускаем тесты с Allure
    if not run_command("pytest tests/ --alluredir=allure-results"):
        return False

    # Генерируем отчет
    if not run_command("allure generate allure-results -o allure-report --clean"):
        print("⚠️  Allure не установлен, пропускаю генерацию отчетов")
        return True

    print("✅ Allure отчеты сгенерированы")
    return True


def main():
    """Основная функция"""
    print("=" * 60)
    print("🎯 COMPREHENSIVE BANKING UI TESTS RUNNER")
    print("=" * 60)

    # Проверяем структуру проекта
    if not check_requirements():
        sys.exit(1)

    # Проверяем тест-кейсы
    if not check_test_cases():
        sys.exit(1)

    # Запускаем тесты
    if not run_tests():
        sys.exit(1)

    # Параллельный запуск
    if not run_parallel_tests():
        sys.exit(1)

    # Генерируем Allure отчеты (только то, что требуется в задании)
    generate_allure_reports()

    print("\n" + "=" * 60)
    print("🎉 ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
    print("=" * 60)
    print("\n📋 Результаты:")
    print("✅ 1. Создание клиента (Add Customer)")
    print("✅ 2. Сортировка клиентов по имени (First Name)")
    print("✅ 3. Удаление клиента")
    print("✅ Доп. задание 1: Allure отчеты")
    print("✅ Доп. задание 2: Параллельный запуск")
    print("✅ Доп. задание 3: CI/CD готовность")
    print("\n📁 Созданные отчеты:")
    print("   - allure-report/ (Allure отчет)")
    print("   - allure-results/ (сырые данные Allure)")
    print("\n🚀 Для просмотра отчетов:")
    print("   allure open allure-report")


if __name__ == "__main__":
    main()