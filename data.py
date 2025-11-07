class URLs:
    """URLs for banking application"""
    BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#"
    MANAGER_PAGE = f"{BASE_URL}/manager"
    CUSTOMER_PAGE = f"{BASE_URL}/customer"
    LOGIN_PAGE = f"{BASE_URL}/login"
    ACCOUNT_PAGE = f"{BASE_URL}/account"
    LIST_CUSTOMERS_PAGE = f"{BASE_URL}/list"


class TestCustomers:
    """Test customer data for banking tests"""

    # Customers for sorting tests
    SORTING_CUSTOMERS = [
        ("Zack", "Anderson", "10001"),
        ("Charlie", "Brown", "10002"),
        ("Alice", "Smith", "10003"),
        ("David", "Wilson", "10004"),
        ("Bob", "Johnson", "10005")
    ]

    # Customers for deletion tests
    DELETE_CUSTOMERS = [
        ("John", "Doe", "20001"),
        ("Christopher", "Nolan", "20002"),
        ("Alex", "Thompson", "20003"),
        ("Michael", "Jackson", "20004")
    ]

    # Valid customer for add tests
    VALID_CUSTOMER = ("Harry", "Potter", "E725JB")


# data.py - добавляем к существующему содержимому

class ApiTestData:
    """Тестовые данные для API тестов"""

    VALID_ENTITY = {
        "title": "Test Entity",
        "description": "Test Description",
        "value": 100,
        "verified": True  # ДОБАВИТЬ
    }

    UPDATE_ENTITY = {
        "title": "Updated Entity",
        "description": "Updated Description",
        "value": 200,
        "verified": False  # ДОБАВИТЬ
    }


class ApiEndpoints:
    """Эндпоинты API"""
    BASE_URL = "http://localhost:8080/api"
    CREATE_ENTITY = f"{BASE_URL}/create"
    DELETE_ENTITY = f"{BASE_URL}/delete/{{id}}"
    GET_ENTITY = f"{BASE_URL}/get/{{id}}"
    GET_ALL_ENTITIES = f"{BASE_URL}/getAll"
    UPDATE_ENTITY = f"{BASE_URL}/patch/{{id}}"


class ApiResponseModels:
    """Модели ответов API"""
    ENTITY_LIST = "entity"
class ApiTestData:
    VALID_ENTITY = {
        'title': 'Test Entity',
        'description': 'Test Description', 
        'value': 100,
        'verified': True
    }
    UPDATE_ENTITY = {
        'title': 'Updated Entity',
        'description': 'Updated Description',
        'value': 200,
        'verified': False
    }
