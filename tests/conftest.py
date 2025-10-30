import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import allure
import time

from data import URLs, TestCustomers  # ✅ ИМПОРТИРУЕМ ИЗ DATA.PY


logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('chromedriver_autoinstaller').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия браузера"""

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)

    except Exception as e:
        logger.error(f"Ошибка при запуске ChromeDriver: {e}")
        raise

    driver.implicitly_wait(0)

    try:
        driver.get(URLs.MANAGER_PAGE)
    except Exception as e:
        logger.error(f"Ошибка при загрузке страницы: {e}")
        raise

    yield driver

    try:
        driver.quit()
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
    """ФИКСТУРА ДЛЯ НАСТРОЙКИ ТЕСТОВ СОРТИРОВКИ"""

    def _setup():
        with allure.step("Создание тестовых клиентов для сортировки"):
            # ✅ ИСПОЛЬЗУЕМ ДАННЫЕ ИЗ DATA.PY
            for first_name, last_name, post_code in TestCustomers.SORTING_CUSTOMERS:
                manager_page.add_customer(first_name, last_name, post_code)
        return manager_page, customers_page

    return _setup


@pytest.fixture
def setup_delete_test(manager_page, customers_page):

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
        except Exception as e:
            logger.error(f"Не удалось сделать скриншот: {e}")