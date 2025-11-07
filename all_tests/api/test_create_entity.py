import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate, AdditionRequest
from data import ApiEndpoints


@allure.feature("API Entity Management")
@allure.story("Создание сущности")
class TestCreateEntity:

    @pytest.mark.api
    @allure.title("Тест создания сущности")
    @allure.testcase("TC-API-001")
    def test_create_entity(self):
        entity_data = EntityCreate(
            title="Тестовая сущность",
            verified=True,
            important_numbers=[42, 87, 15],
            addition=AdditionRequest(
                additional_info="Дополнительные сведения",
                additional_number=123
            )
        )

        response = requests.post(
            ApiEndpoints.CREATE_ENTITY,
            json=entity_data.model_dump(),
            timeout=5
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"

        # API возвращает ID как ЧИСЛО
        created_id = response.json()
        assert isinstance(created_id, int), f"Expected integer ID, got {type(created_id)}: {created_id}"
        assert created_id > 0, f"ID should be positive, got {created_id}"