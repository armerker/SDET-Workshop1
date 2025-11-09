import allure
from typing import Any, List, Dict, Optional, Union


class AssertUtils:
    """Утилиты для проверок в API тестах"""

    @staticmethod
    @allure.step("Проверить статус код ответа")
    def assert_status_code(actual_code: int, expected_code: int, operation: str = "") -> None:
        """
        Проверяет соответствие статус кода

        Args:
            actual_code: Фактический статус код
            expected_code: Ожидаемый статус код
            operation: Описание операции для сообщения об ошибке
        """
        operation_text = f" при операции {operation}" if operation else ""
        assert actual_code == expected_code, (
            f"Ожидался статус код {expected_code}{operation_text}, "
            f"получен {actual_code}"
        )

    @staticmethod
    @allure.step("Проверить тип данных")
    def assert_type(actual_value: Any, expected_type: type, field_name: str = "") -> None:
        """
        Проверяет тип данных

        Args:
            actual_value: Проверяемое значение
            expected_type: Ожидаемый тип
            field_name: Название поля для сообщения об ошибке
        """
        field_text = f" поля '{field_name}'" if field_name else ""
        assert isinstance(actual_value, expected_type), (
            f"Ожидался тип {expected_type}{field_text}, "
            f"получен {type(actual_value)}: {actual_value}"
        )

    @staticmethod
    @allure.step("Проверить что значение положительное")
    def assert_positive(value: int, field_name: str = "") -> None:
        """
        Проверяет что число положительное

        Args:
            value: Проверяемое число
            field_name: Название поля для сообщения об ошибке
        """
        field_text = f" поля '{field_name}'" if field_name else ""
        assert value > 0, (
            f"Значение{field_text} должно быть положительным, получено {value}"
        )

    @staticmethod
    @allure.step("Проверить наличие поля в ответе")
    def assert_field_exists(data: Dict, field_name: str, context: str = "") -> None:
        """
        Проверяет наличие поля в словаре

        Args:
            data: Словарь с данными
            field_name: Имя поля
            context: Контекст для сообщения об ошибке
        """
        context_text = f" в {context}" if context else ""
        assert field_name in data, (
            f"Поле '{field_name}' отсутствует{context_text}. "
            f"Доступные поля: {list(data.keys())}"
        )

    @staticmethod
    @allure.step("Проверить равенство значений")
    def assert_equal(actual_value: Any, expected_value: Any, field_name: str = "") -> None:
        """
        Проверяет равенство двух значений

        Args:
            actual_value: Фактическое значение
            expected_value: Ожидаемое значение
            field_name: Название поля для сообщения об ошибке
        """
        field_text = f" поля '{field_name}'" if field_name else ""
        assert actual_value == expected_value, (
            f"Значение{field_text} не совпадает. "
            f"Ожидалось: {expected_value}, получено: {actual_value}"
        )

    @staticmethod
    @allure.step("Проверить наличие значения в списке")
    def assert_in_list(item: Any, item_list: List, context: str = "") -> None:
        """
        Проверяет наличие элемента в списке

        Args:
            item: Искомый элемент
            item_list: Список для поиска
            context: Контекст для сообщения об ошибке
        """
        context_text = f" {context}" if context else ""
        assert item in item_list, (
            f"Элемент {item} не найден{context_text}. "
            f"Доступные элементы: {item_list}"
        )

    @staticmethod
    @allure.step("Проверить отсутствие значения в списке")
    def assert_not_in_list(item: Any, item_list: List, context: str = "") -> None:
        """
        Проверяет отсутствие элемента в списке

        Args:
            item: Элемент который не должен быть в списке
            item_list: Список для проверки
            context: Контекст для сообщения об ошибке
        """
        context_text = f" {context}" if context else ""
        assert item not in item_list, (
            f"Элемент {item} не должен присутствовать{context_text}, "
            f"но найден в списке: {item_list}"
        )

    @staticmethod
    @allure.step("Проверить структуру ответа API")
    def assert_api_response_structure(response_data: Dict, expected_fields: List[str]) -> None:
        """
        Проверяет наличие ожидаемых полей в ответе API

        Args:
            response_data: Данные ответа
            expected_fields: Список ожидаемых полей
        """
        missing_fields = [field for field in expected_fields if field not in response_data]
        assert len(missing_fields) == 0, (
            f"В ответе API отсутствуют обязательные поля: {missing_fields}. "
            f"Доступные поля: {list(response_data.keys())}"
        )

    @staticmethod
    @allure.step("Проверить что список не пустой")
    def assert_list_not_empty(item_list: List, list_name: str = "") -> None:
        """
        Проверяет что список не пустой

        Args:
            item_list: Проверяемый список
            list_name: Название списка для сообщения об ошибке
        """
        list_text = f" '{list_name}'" if list_name else ""
        assert len(item_list) > 0, f"Список{list_text} не должен быть пустым"

    @staticmethod
    @allure.step("Проверить статус код из списка допустимых")
    def assert_status_code_in(actual_code: int, expected_codes: List[int], operation: str = "") -> None:
        """
        Проверяет что статус код находится в списке допустимых

        Args:
            actual_code: Фактический статус код
            expected_codes: Список ожидаемых статус кодов
            operation: Описание операции для сообщения об ошибке
        """
        operation_text = f" при операции {operation}" if operation else ""
        assert actual_code in expected_codes, (
            f"Ожидался один из статус кодов {expected_codes}{operation_text}, "
            f"получен {actual_code}"
        )


# Создаем экземпляр для удобного импорта
assert_utils = AssertUtils()