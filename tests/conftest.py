import pytest
import logging
import platform
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure

from data import URLs, TestCustomers

logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('webdriver_manager').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


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