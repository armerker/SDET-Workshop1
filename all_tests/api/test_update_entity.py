import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints


@allure.feature("API Entity Management")
@allure.story("Обновление сущности")
class TestUpdateEntity:

    @pytest.mark.api
    @allure.title("Тест обновления сущности")
    @allure.testcase("TC-API-004")
    def test_update_entity(self):
        # Создаем сущность для обновления
        create_data = EntityCreate(
            title="Исходный заголовок",
            verified=False,
            important_numbers=[10, 20, 30]
        )

        create_response = requests.post(
            ApiEndpoints.CREATE_ENTITY,
            json=create_data.model_dump(),
            timeout=5
        )
        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        entity_id = create_response.json()

        # Обновляем сущность
        update_data = {
            "title": "Обновленный заголовок",
            "verified": True,
            "important_numbers": [99, 88, 77],
            "addition": {
                "additional_info": "Обновленная информация",
                "additional_number": 999
            }
        }

        update_response = requests.patch(
            ApiEndpoints.UPDATE_ENTITY.format(id=entity_id),
            json=update_data,
            timeout=5
        )

        # PATCH может возвращать 200 или 204
        assert update_response.status_code in [200, 204], f"PATCH failed: {update_response.text}"

        # Если вернулся контент - проверяем его
        if update_response.status_code == 200:
            updated_entity = update_response.json()
            assert updated_entity["title"] == "Обновленный заголовок"