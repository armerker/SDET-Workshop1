import pytest
import allure
from pages.manager_page import ManagerPage
from pages.customers_page import CustomersPage
from utils.test_data_generator import TestDataGenerator


@allure.feature("Удаление клиента")
@allure.story("Удаление клиента с длиной имени, близкой к средней")
class TestDeleteCustomer:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.manager_page = ManagerPage(driver)
        self.customers_page = CustomersPage(driver)

        # Создаем тестовых клиентов с разной длиной имен
        with allure.step("Создание тестовых клиентов с разной длиной имен"):
            test_customers = [
                ("Al", "Short", "1111111111"),  # длина 2
                ("Neville", "Medium", "2222222222"),  # длина 7
                ("Voldemort", "Long", "3333333333")  # длина 9
            ]

            for first_name, last_name, post_code in test_customers:
                self.manager_page.add_customer(first_name, last_name, post_code)

    @pytest.mark.regression
    @allure.title("Тест удаления клиента с длиной имени, близкой к средней")
    def test_delete_customer_closest_to_average_name_length(self, driver):
        with allure.step("Переход на страницу клиентов"):
            self.manager_page.click_customers()

        with allure.step("Получение списка всех имен клиентов"):
            customer_names = self.customers_page.get_customer_names()
            allure.attach(str(customer_names), name="Customer Names", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Вычисление средней длины имен и поиск клиента для удаления"):
            customer_to_delete = TestDataGenerator.find_closest_to_average_name(customer_names)

            # Вычисляем длины для отчета
            name_lengths = [len(name) for name in customer_names]
            average_length = sum(name_lengths) / len(name_lengths)

            allure.attach(
                f"Names: {customer_names}\nLengths: {name_lengths}\nAverage: {average_length:.2f}\nTo delete: {customer_to_delete}",
                name="Name Length Analysis",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Удаление выбранного клиента"):
            delete_result = self.customers_page.delete_customer_by_name(customer_to_delete)
            assert delete_result, f"Failed to delete customer: {customer_to_delete}"

        with allure.step("Проверка, что клиент удален"):
            remaining_names = self.customers_page.get_customer_names()
            assert customer_to_delete not in remaining_names, \
                f"Customer {customer_to_delete} was not deleted. Remaining: {remaining_names}"

            allure.attach(str(remaining_names), name="Remaining Customers", attachment_type=allure.attachment_type.TEXT)