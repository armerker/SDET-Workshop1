from selenium.webdriver.common.by import By
from .base_page import BasePage


class CustomersPage(BasePage):
    # Locators
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search Customer']")
    FIRST_NAME_HEADER = (By.XPATH, "//a[contains(text(),'First Name')]")

    # Customer table
    CUSTOMER_ROWS = (By.XPATH, "//table[@class='table table-bordered table-striped']//tbody/tr")
    DELETE_BUTTONS = (By.XPATH, "//button[contains(text(),'Delete')]")

    # Customer row elements
    FIRST_NAME_CELL = (By.XPATH, "./td[1]")
    LAST_NAME_CELL = (By.XPATH, "./td[2]")
    POST_CODE_CELL = (By.XPATH, "./td[3]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_customer_names(self):
        """Получает список всех имен клиентов из таблицы"""
        rows = self.find_elements(self.CUSTOMER_ROWS)
        names = []

        for row in rows:
            first_name_cell = row.find_element(*self.FIRST_NAME_CELL)
            names.append(first_name_cell.text)

        return names

    def sort_by_first_name(self):
        """Кликает на заголовок First Name для сортировки"""
        self.click(self.FIRST_NAME_HEADER)

    def delete_customer_by_name(self, name):
        """Удаляет клиента по имени"""
        rows = self.find_elements(self.CUSTOMER_ROWS)

        for i, row in enumerate(rows):
            first_name_cell = row.find_element(*self.FIRST_NAME_CELL)
            if first_name_cell.text == name:
                delete_buttons = self.find_elements(self.DELETE_BUTTONS)
                delete_buttons[i].click()
                return True

        return False

    def is_customer_present(self, name):
        """Проверяет, присутствует ли клиент с указанным именем"""
        names = self.get_customer_names()
        return name in names

    def get_sorted_names(self):
        """Возвращает отсортированный список имен для проверки сортировки"""
        return sorted(self.get_customer_names())