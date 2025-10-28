import pytest
import allure
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.manager_page import ManagerPage
from pages.customers_page import CustomersPage
from utils.test_data_generator import TestDataGenerator


@allure.feature("Сортировка клиентов")
@allure.story("Проверка сортировки клиентов по имени")
class TestCustomerSorting:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.manager_page = ManagerPage(driver)
        self.customers_page = CustomersPage(driver)

        # Создаем тестовых клиентов для сортировки
        with allure.step("Создание тестовых клиентов"):
            test_customers = [
                ("Harry", "Potter", "1234567890"),
                ("Albus", "Dumbledore", "2345678901"),
                ("Severus", "Snape", "3456789012")
            ]

            for first_name, last_name, post_code in test_customers:
                self.manager_page.add_customer(first_name, last_name, post_code)

    @pytest.mark.regression
    @allure.title("Тест сортировки клиентов по имени в алфавитном порядке")
    def test_sort_customers_by_first_name(self, driver):
        with allure.step("Переход на страницу клиентов"):
            self.manager_page.click_customers()

        with allure.step("Получение исходного списка имен"):
            original_names = self.customers_page.get_customer_names()
            print(f"Исходный порядок: {original_names}")

        with allure.step("Сортировка по убыванию (Z-A) - первый клик"):
            self.customers_page.sort_by_first_name()
            sorted_names_desc = self.customers_page.get_customer_names()
            expected_sorted_desc = sorted(original_names, reverse=True)
            print(f"После первого клика (Z-A): {sorted_names_desc}")

            # Проверяем сортировку Z-A
            assert sorted_names_desc == expected_sorted_desc, \
                f"Sorting Z-A failed. Expected: {expected_sorted_desc}, Got: {sorted_names_desc}"

        with allure.step("Сортировка по возрастанию (A-Z) - второй клик"):
            self.customers_page.sort_by_first_name()
            sorted_names_asc = self.customers_page.get_customer_names()
            expected_sorted_asc = sorted(original_names)
            print(f"После второго клика (A-Z): {sorted_names_asc}")

            # Проверяем сортировку A-Z
            assert sorted_names_asc == expected_sorted_asc, \
                f"Sorting A-Z failed. Expected: {expected_sorted_asc}, Got: {sorted_names_asc}"

        print("✅ Сортировка работает правильно: Z-A → A-Z")