import pytest
import logging
import platform
import os
from typing import Generator, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure

from data import URLs, TestCustomers
from all_tests.api.clients.api_client import APIClient
from all_tests.api.utils.data_generator import DataGenerator
from all_tests.api.models.entity_models import EntityCreate
from all_tests.api.models.response_model import CreateEntityResponse, EntityResponse

# Настройка логирования
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('webdriver_manager').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

# ==================== UI ФИКСТУРЫ (SELENIUM) ====================

def get_chrome_options():
    """Создает настройки Chrome для разных ОС"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")

    # Для CI/CD - headless, для локально - headed
    if os.getenv('CI') or os.getenv('GITHUB_ACTIONS'):
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--headed")

    return chrome_options


@pytest.fixture(scope="function")
def driver():
    """Универсальная фикстура для Windows и Linux"""

    chrome_options = get_chrome_options()
    current_os = platform.system()

    try:
        # Вариант 1: Используем webdriver-manager для автоматической установки
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info(f"ChromeDriver успешно запущен через webdriver-manager на {current_os}")

    except Exception as e:
        logger.error(f"Webdriver-manager не сработал: {e}")

        # Вариант 2: Пробуем системный Chrome
        try:
            logger.info("Пробуем системный Chrome")
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome запущен напрямую")
        except Exception as fallback_error:
            logger.error(f"Системный Chrome не сработал: {fallback_error}")

            # Вариант 3: Для Windows - пробуем разные пути
            if current_os == "Windows":
                try:
                    common_paths = [
                        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    ]

                    for path in common_paths:
                        if os.path.exists(path):
                            chrome_options.binary_location = path
                            driver = webdriver.Chrome(options=chrome_options)
                            logger.info(f"Chrome найден по пути: {path}")
                            break
                    else:
                        raise Exception("Chrome не найден в стандартных путях")

                except Exception as windows_error:
                    logger.error(f"Windows пути не сработали: {windows_error}")
                    raise
            else:
                # Для Linux пробуем Chromium
                try:
                    chrome_options.binary_location = "/usr/bin/chromium-browser"
                    service = Service("/usr/bin/chromedriver")
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    logger.info("Chromium запущен на Linux")
                except Exception as linux_error:
                    logger.error(f"Chromium не сработал: {linux_error}")
                    raise

    driver.implicitly_wait(0)

    try:
        driver.get(URLs.MANAGER_PAGE)
        logger.info(f"Загружена страница: {URLs.MANAGER_PAGE}")
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы: {e}")
        raise

    yield driver

    try:
        driver.quit()
        logger.info("Браузер закрыт")
    except Exception as e:
        logger.error(f"Ошибка при закрытии браузера: {e}")


@pytest.fixture
def manager_page(driver):
    """Фикстура для страницы менеджера"""
    from pages.manager_page import ManagerPage
    return ManagerPage(driver)


@pytest.fixture
def customers_page(driver):
    """Фикстура для страницы клиентов"""
    from pages.customers_page import CustomersPage
    return CustomersPage(driver)


@pytest.fixture
def setup_sorting_test(manager_page, customers_page):
    """Фикстура для настройки тестов сортировки"""

    def _setup():
        with allure.step("Создание тестовых клиентов для сортировки"):
            for first_name, last_name, post_code in TestCustomers.SORTING_CUSTOMERS:
                manager_page.add_customer(first_name, last_name, post_code)
        return manager_page, customers_page

    return _setup


@pytest.fixture
def setup_delete_test(manager_page, customers_page):
    """Фикстура для настройки тестов удаления"""

    def _setup():
        with allure.step("Создание тестовых клиентов с разной длиной имен"):
            for first_name, last_name, post_code in TestCustomers.DELETE_CUSTOMERS:
                manager_page.add_customer(first_name, last_name, post_code)
        return manager_page, customers_page

    return _setup


# ==================== API ФИКСТУРЫ ====================

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Фикстура для API клиента (на всю сессию)"""
    client = APIClient()
    logger.info("API клиент инициализирован")
    return client


@pytest.fixture(scope="session")
def data_generator() -> DataGenerator:
    """Фикстура для генератора данных (на всю сессию)"""
    generator = DataGenerator()
    logger.info("Генератор данных инициализирован")
    return generator


@pytest.fixture
def random_entity_data(data_generator: DataGenerator) -> EntityCreate:
    """Фикстура для случайных данных сущности"""
    return data_generator.generate_entity_create_data()


@pytest.fixture
def simple_entity_data(data_generator: DataGenerator) -> EntityCreate:
    """Фикстура для простых данных сущности (без дополнений)"""
    return data_generator.generate_entity_create_data(
        title="Тестовая сущность",
        verified=True,
        with_addition=False
    )


@pytest.fixture
def entity_with_addition_data(data_generator: DataGenerator) -> EntityCreate:
    """Фикстура для данных сущности с дополнительной информацией"""
    return data_generator.generate_entity_create_data(
        title="Сущность с дополнением",
        verified=False,
        with_addition=True
    )


@pytest.fixture
def test_entity(api_client: APIClient, random_entity_data: EntityCreate) -> Generator[int, None, None]:
    with allure.step("Создание тестовой сущности через фикстуру"):
        create_response = api_client.post(
            "create",
            random_entity_data,
            CreateEntityResponse
        )
        entity_id = create_response.id  # ← Теперь берем .id из объекта

    yield entity_id

    # Пост-очистка: удаляем созданную сущность
    with allure.step("Очистка: удаление тестовой сущности"):
        try:
            api_client.delete(f"delete/{entity_id}")
            logger.info(f"Удалена тестовая сущность ID: {entity_id}")
        except Exception as e:
            logger.warning(f"Ошибка при удалении сущности {entity_id}: {e}")


@pytest.fixture
def multiple_test_entities(api_client: APIClient, data_generator: DataGenerator) -> Generator[List[int], None, None]:
    """
    Фикстура для создания нескольких тестовых сущностей

    Returns:
        List[int]: Список ID созданных сущностей
    """
    entities_data = data_generator.generate_multiple_entities(count=3)
    created_ids = []

    with allure.step("Создание нескольких тестовых сущностей через фикстуру"):
        for i, entity_data in enumerate(entities_data):
            create_response = api_client.post(
                "create",
                entity_data,
                CreateEntityResponse
            )
            created_ids.append(create_response.id)
            logger.info(f"Создана сущность {i+1}/3 ID: {create_response.id}")

    yield created_ids

    # Пост-очистка: удаляем все созданные сущности
    with allure.step("Очистка: удаление нескольких тестовых сущностей"):
        for entity_id in created_ids:
            try:
                api_client.delete(f"delete/{entity_id}")
                logger.info(f"Удалена сущность ID: {entity_id}")
            except Exception as e:
                logger.warning(f"Ошибка при удалении сущности {entity_id}: {e}")


@pytest.fixture
def entity_for_update(api_client: APIClient, data_generator: DataGenerator) -> Generator[int, None, None]:
    """
    Фикстура для сущности, предназначенной для тестов обновления

    Returns:
        int: ID созданной сущности
    """
    entity_data = data_generator.generate_entity_create_data(
        title="Сущность для обновления",
        verified=False
    )

    create_response = api_client.post(
        "create",
        entity_data,
        CreateEntityResponse
    )
    entity_id = create_response.id
    logger.info(f"Создана сущность для обновления ID: {entity_id}")

    yield entity_id

    try:
        api_client.delete(f"delete/{entity_id}")
        logger.info(f"Удалена сущность для обновления ID: {entity_id}")
    except Exception as e:
        logger.warning(f"Ошибка при удалении сущности для обновления {entity_id}: {e}")


@pytest.fixture
def entity_for_deletion(api_client: APIClient, data_generator: DataGenerator) -> int:
    """
    Фикстура для сущности, предназначенной для тестов удаления
    (без очистки, так как тест сам удаляет сущность)

    Returns:
        int: ID созданной сущности
    """
    entity_data = data_generator.generate_entity_create_data(
        title="Сущность для удаления",
        verified=True
    )

    create_response = api_client.post(
        "create",
        entity_data,
        CreateEntityResponse
    )
    entity_id = create_response.id
    logger.info(f"Создана сущность для удаления ID: {entity_id}")

    return entity_id


# ==================== ОБЩИЕ ФИКСТУРЫ ====================

@pytest.fixture(autouse=True)
def log_test_start(request):
    """Автоматическая фикстура для логирования начала теста"""
    test_name = request.node.name
    logger.info(f"=== Начало теста: {test_name} ===")
    yield
    logger.info(f"=== Конец теста: {test_name} ===")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.funcargs:
                driver = item.funcargs['driver']
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info("Сделан скриншот при падении теста")
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {e}")