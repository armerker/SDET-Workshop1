# Banking UI Tests

# Banking UI Tests

Автотесты для Banking Project на Python с использованием Selenium WebDriver и pytest.

## Функциональности

- ✅ Создание клиента с генерацией данных по спецификации
- ✅ Сортировка клиентов по имени  
- ✅ Удаление клиента по средней длине имени
- 📊 Allure отчёты
- 🔄 Параллельный запуск тестов
- ⚙️ CI/CD интеграция

## Чек‑лист тестов

1. **Создание клиента (Add Customer)**:
   - генерация 10‑значного Post Code;
   - генерация First Name на основе Post Code;
   - проверка успешного создания.

2. **Сортировка клиентов по имени (First Name)**:
   - сортировка A–Z;
   - сортировка Z–A.

3. **Удаление клиента**:
   - поиск клиента с длиной имени, близкой к средней;
   - удаление выбранного клиента.

## Установка и настройка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd banking-ui-tests
2. Создание виртуального окружения
bash
# Для Windows
python -m venv .venv
.venv\Scripts\activate

# Для Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
3. Установка зависимостей
bash
pip install --upgrade pip
pip install -r requirements.txt
4. Установка Chrome и ChromeDriver
bash
# Автоматическая установка (через chromedriver-autoinstaller)
# При первом запуске тестов ChromeDriver установится автоматически

# Ручная установка (опционально):
# Скачайте ChromeDriver с https://chromedriver.chromium.org/
# Добавьте в PATH или укажите путь в коде
5. Запуск тестов
bash
# Запуск всех тестов
pytest tests/ -v

# Запуск с детальным выводом
pytest tests/ -v -s

# Запуск конкретного теста
pytest tests/test_add_customer.py -v
pytest tests/test_customer_sorting.py -v
pytest tests/test_delete_customer.py -v

# Парралельное тестирование

pytest tests/ -n auto --tb=short

# Запуск по маркерам
pytest tests/ -m smoke -v
pytest tests/ -m regression -v
6. Генерация Allure отчётов
bash
# Запуск тестов с генерацией Allure результатов
pytest tests/ -v --alluredir=allure-results

# Генерация и просмотр отчёта
allure serve allure-results

# Генерация статического отчёта
allure generate allure-results -o allure-report --clean
Просмотр отчётов
Локальный просмотр
bash
# После запуска тестов с Allure
allure serve allure-results
Откроется браузер с подробным отчётом: http://localhost:8080

Структура отчёта
Overview: общая статистика по тестам;

Suites: группировка тестов по сьютам;

Graphs: графики и метрики;

Timeline: временная шкала выполнения.

CI/CD Интеграция
GitHub Actions
При каждом пуше в main/master ветку автоматически запускаются тесты и генерируется Allure отчёт.

Просмотр отчёта в CI
После завершения CI пайплайна:

Перейдите в Actions в вашем репозитории

Выберите последний запуск workflow

В разделе Artifacts скачайте allure-report

Распакуйте и откройте index.html в браузере

Или используйте Allure Action для автоматической публикации:

yaml
- name: Publish Allure Report
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_branch: gh-pages
    publish_dir: allure-report
После настройки отчёт будет доступен по адресу:
https://<your-username>.github.io/<repository-name>/

Пример успешного запуска в CI
https://github.com/%3Cusername%3E/%3Crepository%3E/actions/workflows/test.yml/badge.svg

Структура проекта
text
banking-ui-tests/
├── tests/                    # Тестовые файлы
│   ├── test_add_customer.py     # Тесты создания клиента
│   ├── test_customer_sorting.py # Тесты сортировки
│   └── test_delete_customer.py  # Тесты удаления
├── pages/                   # Page Object модели
│   ├── base_page.py            # Базовый класс страницы
│   ├── manager_page.py         # Страница менеджера
│   └── customers_page.py       # Страница клиентов
├── utils/                   # Вспомогательные утилиты
│   └── test_data_generator.py  # Генератор тестовых данных
├── conftest.py             # Фикстуры pytest
├── pytest.ini              # Конфигурация pytest
├── requirements.txt        # Зависимости проекта
└── README.md              # Документация