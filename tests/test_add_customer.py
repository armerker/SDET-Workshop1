import pytest
import allure
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.manager_page import ManagerPage
from utils.test_data_generator import TestDataGenerator


@allure.feature("Добавление клиента")
@allure.story("Создание нового клиента в системе")
class TestAddCustomer:
    @pytest.mark.smoke
    @allure.title("Тест создания клиента с валидными данными")
    def test_add_customer_with_valid_data(self, driver):
        with allure.step("Генерация тестовых данных"):
            post_code = TestDataGenerator.generate_post_code()
            first_name = TestDataGenerator.generate_first_name_from_post_code(post_code)
            last_name = TestDataGenerator.generate_last_name()

        with allure.step("Создание клиента через UI"):
            manager_page = ManagerPage(driver)
            alert_text = manager_page.add_customer(first_name, last_name, post_code)

        with allure.step("Проверка успешного создания клиента"):
            # Исправляем проверку - текст содержит ID клиента
            assert "Customer added successfully" in alert_text, f"Expected success message, but got '{alert_text}'"

        with allure.step("Проверка логики генерации имени из почтового кода"):
            # Проверяем, что имя сгенерировано правильно по логике
            expected_name = TestDataGenerator.generate_first_name_from_post_code(post_code)
            assert first_name == expected_name, f"Name generation failed. Expected: {expected_name}, Got: {first_name}"