"""Файл с URL и константами"""


class URLs:
    """Класс для хранения URL"""
    BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject"
    MANAGER_PAGE = f"{BASE_URL}/#/manager"
    CUSTOMER_PAGE = f"{BASE_URL}/#/customer"
    LOGIN_PAGE = f"{BASE_URL}/#/login"


class TestCustomers:
    """Класс для хранения тестовых данных клиентов"""

    # Для тестов сортировки
    SORTING_CUSTOMERS = [
        ("Harry", "Potter", "1234567890"),
        ("Albus", "Dumbledore", "2345678901"),
        ("Severus", "Snape", "3456789012")
    ]

    # Для тестов удаления (с разной длиной имен)
    DELETE_CUSTOMERS = [
        ("Al", "Short", "1111111111"),
        ("Neville", "Medium", "2222222222"),
        ("Voldemort", "Long", "3333333333")
    ]