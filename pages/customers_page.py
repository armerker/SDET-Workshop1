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
<<<<<<< HEAD
        """Получает список всех имен клиентов из таблицы"""
=======
        """Оптимизированное получение списка имен клиентов."""
>>>>>>> develop
        rows = self.find_elements(self.CUSTOMER_ROWS)
        names = []

        for row in rows:
<<<<<<< HEAD
            first_name_cell = row.find_element(*self.FIRST_NAME_CELL)
            names.append(first_name_cell.text)
=======
            try:
                first_name_cell = row.find_element(*self.FIRST_NAME_CELL)
                names.append(first_name_cell.text)
            except Exception:
                continue  # Пропускаем проблемные строки
>>>>>>> develop

        return names

    def sort_by_first_name(self):
<<<<<<< HEAD
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
=======
        """Быстрая сортировка по имени."""
        self.click(self.FIRST_NAME_HEADER)

    def delete_customer_by_name(self, name):
        """Оптимизированное удаление клиента по имени."""
        rows = self.find_elements(self.CUSTOMER_ROWS)

        for i, row in enumerate(rows):
            try:
                first_name_cell = row.find_element(*self.FIRST_NAME_CELL)
                if first_name_cell.text == name:
                    delete_btn = row.find_element(By.XPATH, ".//button[contains(text(),'Delete')]")
                    delete_btn.click()
                    return True
            except Exception as e:
                print(f"Ошибка при удалении клиента {name}: {e}")
                continue
>>>>>>> develop

        return False

    def is_customer_present(self, name):
<<<<<<< HEAD
        """Проверяет, присутствует ли клиент с указанным именем"""
=======
        """Быстрая проверка наличия клиента."""
>>>>>>> develop
        names = self.get_customer_names()
        return name in names

    def get_sorted_names(self):
<<<<<<< HEAD
        """Возвращает отсортированный список имен для проверки сортировки"""
=======
        """Быстрое получение отсортированного списка."""
>>>>>>> develop
        return sorted(self.get_customer_names())