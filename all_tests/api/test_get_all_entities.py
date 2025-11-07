import pytest
import allure
import requests
from data import ApiEndpoints, ApiResponseModels


@allure.feature("API Entity Management")
@allure.story("Получение всех сущностей")
class TestGetAllEntities:

    @pytest.mark.api
    @allure.title("Тест получения всех сущностей")
    @allure.testcase("TC-API-003")
    def test_get_all_entities(self):
        response = requests.post(
            ApiEndpoints.GET_ALL_ENTITIES,
            timeout=5
        )
        assert response.status_code == 200, f"GetAll failed: {response.text}"
        response_data = response.json()
        assert ApiResponseModels.ENTITY_LIST in response_data
        assert isinstance(response_data[ApiResponseModels.ENTITY_LIST], list)