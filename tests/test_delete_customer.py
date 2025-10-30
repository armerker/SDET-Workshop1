import pytest
import allure
import logging
from utils.test_data_generator import TestDataGenerator

logger = logging.getLogger(__name__)


@allure.feature("Удаление клиента")
@allure.story("Удаление клиента с длиной имени, близкой к средней")
class TestDeleteCustomer:

    @pytest.mark.regression
    @allure.title("Тест удаления клиента с длиной имени, близкой к средней")
    @allure.testcase("TC-003")
    def test_delete_customer_closest_to_average_name_length(self, setup_delete_test):

        try:
            # Получаем настроенные страницы из фикстуры
            manager_page, customers_page = setup_delete_test()

            with allure.step("Переход на страницу клиентов"):
                manager_page.click_customers()

            with allure.step("Получение списка всех имен клиентов"):
                customer_names = customers_page.get_customer_names()
                allure.attach(str(customer_names), name="Customer Names", attachment_type=allure.attachment_type.TEXT)

            with allure.step("Вычисление средней длины имен и поиск клиента для удаления"):
                customer_to_delete = TestDataGenerator.find_closest_to_average_name(customer_names)

                name_lengths = [len(name) for name in customer_names]
                average_length = sum(name_lengths) / len(name_lengths)

                allure.attach(
                    f"Names: {customer_names}\nLengths: {name_lengths}\nAverage: {average_length:.2f}\nTo delete: {customer_to_delete}",
                    name="Name Length Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )

            with allure.step("Удаление выбранного клиента"):
                delete_result = customers_page.delete_customer_by_name(customer_to_delete)
                assert delete_result, f"Failed to delete customer: {customer_to_delete}"

            with allure.step("Проверка, что клиент удален"):
                remaining_names = customers_page.get_customer_names()
                assert customer_to_delete not in remaining_names, \
                    f"Customer {customer_to_delete} was not deleted. Remaining: {remaining_names}"

                allure.attach(str(remaining_names), name="Remaining Customers",
                              attachment_type=allure.attachment_type.TEXT)

        except Exception as e:
            logger.error(f"Тест удаления клиента упал с ошибкой: {e}")
            raise