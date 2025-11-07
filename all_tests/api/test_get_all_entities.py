import pytest
import allure
import requests
from data import ApiEndpoints


@allure.feature("API Entity Management")
@allure.story("Получение всех сущностей")
class TestGetAllEntities:

    @pytest.mark.api
    @allure.title("Тест получения всех сущностей")
    @allure.testcase("TC-API-003")
    def test_get_all_entities(self):
        # GET запрос
        response = requests.get(
            ApiEndpoints.GET_ALL_ENTITIES,
            timeout=5
        )
        assert response.status_code == 200, f"GetAll failed: {response.text}"

        # API возвращает объект с полем "entity"
        response_data = response.json()
        assert isinstance(response_data, dict), f"Expected dict, got {type(response_data)}"
        assert "entity" in response_data, f"Field 'entity' not found in response"
        assert isinstance(response_data["entity"], list), f"Expected list in 'entity' field"