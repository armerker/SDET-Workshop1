import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints


@allure.feature("API Entity Management")
@allure.story("Удаление сущности")
class TestDeleteEntity:

    @pytest.mark.api
    @allure.title("Тест удаления сущности")
    @allure.testcase("TC-API-005")
    def test_delete_entity(self):
        # Создаем сущность
        create_data = EntityCreate(
            title="Entity to Delete",
            description="To be deleted",
            value=100,
            verified=True
        )
        create_response = requests.post(
            ApiEndpoints.CREATE_ENTITY,
            json=create_data.model_dump(),
            timeout=5
        )
        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        created_id = create_response.json()

        # Удаляем сущность
        delete_response = requests.delete(
            ApiEndpoints.DELETE_ENTITY.format(id=created_id),
            timeout=5
        )
        # DELETE возвращает 204 (No Content)
        assert delete_response.status_code == 204, f"Expected 204, got {delete_response.status_code}"