from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple, Any, Optional
import logging


class BasePage:
    """Базовый класс для всех Page Object моделей.

    Предоставляет общие методы для работы с веб-элементами
    и ожиданиями в Selenium WebDriver.

    Attributes:
        driver: Экземпляр WebDriver для управления браузером.
        wait: Объект для явных ожиданий с таймаутом 10 секунд.
    """

    def __init__(self, driver: WebDriver) -> None:
        """Инициализирует базовую страницу.

        Args:
            driver: Экземпляр WebDriver для управления браузером.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Находит элемент на странице с ожиданием его присутствия в DOM.

        Args:
            locator: Кортеж (By стратегия, локатор) для поиска элемента.

        Returns:
            Найденный веб-элемент.

        Raises:
            TimeoutException: Если элемент не найден в течение таймаута.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Находит все элементы на странице с ожиданием их присутствия в DOM.

        Args:
            locator: Кортеж (By стратегия, локатор) для поиска элементов.

        Returns:
            Список найденных веб-элементов.

        Raises:
            TimeoutException: Если элементы не найдены в течение таймаута.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        """Кликает на элемент после ожидания его кликабельности.

        Args:
            locator: Кортеж (By стратегия, локатор) для поиска элемента.

        Raises:
            TimeoutException: Если элемент не становится кликабельным в течение таймаута.
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """Очищает поле ввода и вводит текст после ожидания кликабельности элемента.

        Args:
            locator: Кортеж (By стратегия, локатор) для поиска элемента.
            text: Текст для ввода в поле.

        Raises:
            TimeoutException: Если элемент не становится кликабельным в течение таймаута.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def get_alert_text(self) -> Optional[str]:
        """Ожидает появление alert, получает его текст и подтверждает.

        Returns:
            Текст alert или None, если alert не появился.

        Raises:
            TimeoutException: Если alert не появляется в течение таймаута.
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Проверяет наличие элемента на странице без выброса исключения.

        Args:
            locator: Кортеж (By стратегия, локатор) для поиска элемента.

        Returns:
            True если элемент присутствует, False в противном случае.
        """
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False

    def wait_for_alert(self, timeout: int = 10) -> Any:
        """Явно ожидает появление alert на странице.

        Args:
            timeout: Время ожидания в секундах (по умолчанию 10).

        Returns:
            Объект alert.

        Raises:
            TimeoutException: Если alert не появляется в течение указанного времени.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.alert_is_present())