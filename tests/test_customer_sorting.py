import pytest
import allure
import logging
from utils.test_data_generator import TestDataGenerator

logger = logging.getLogger(__name__)


@allure.feature("Сортировка клиентов")
@allure.story("Проверка сортировки клиентов по имени")
class TestCustomerSorting:
    @pytest.mark.ui
    @pytest.mark.regression
    @allure.title("Тест сортировки клиентов по имени в алфавитном порядке")
    @allure.testcase("TC-002")
    def test_sort_customers_by_first_name(self, setup_sorting_test):
        manager_page, customers_page = setup_sorting_test()

        with allure.step("Переход на страницу клиентов"):
            manager_page.click_customers()

        with allure.step("Получение исходного списка имен"):
            original_names = customers_page.get_customer_names()

        with allure.step("Сортировка по убыванию (Z-A) - первый клик"):
            customers_page.sort_by_first_name()
            sorted_names_desc = customers_page.get_customer_names()
            expected_sorted_desc = sorted(original_names, reverse=True)

            assert sorted_names_desc == expected_sorted_desc, \
                f"Sorting Z-A failed. Expected: {expected_sorted_desc}, Got: {sorted_names_desc}"

        with allure.step("Сортировка по возрастанию (A-Z) - второй клик"):
            customers_page.sort_by_first_name()
            sorted_names_asc = customers_page.get_customer_names()
            expected_sorted_asc = sorted(original_names)

            assert sorted_names_asc == expected_sorted_asc, \
                f"Sorting A-Z failed. Expected: {expected_sorted_asc}, Got: {sorted_names_asc}"