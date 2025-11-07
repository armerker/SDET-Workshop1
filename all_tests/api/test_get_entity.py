import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints


@allure.feature("API Entity Management")
@allure.story("Получение сущности по ID")
class TestGetEntity:

    @pytest.mark.api
    @allure.title("Тест получения сущности по ID")
    @allure.testcase("TC-API-002")
    def test_get_entity(self):
        # Создаем сущность
        create_data = EntityCreate(
            title="Тест получения сущности",
            verified=True,
            important_numbers=[1, 2, 3]
        )
        create_response = requests.post(
            ApiEndpoints.CREATE_ENTITY,
            json=create_data.model_dump(),
            timeout=5
        )
        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        created_id = create_response.json()

        # Получаем сущность по ID
        get_response = requests.get(
            ApiEndpoints.GET_ENTITY.format(id=created_id),
            timeout=5
        )
        assert get_response.status_code == 200, f"Get failed: {get_response.text}"

        retrieved_entity = get_response.json()
        assert retrieved_entity["id"] == created_id
        assert retrieved_entity["title"] == create_data.title
        assert retrieved_entity["verified"] == create_data.verified