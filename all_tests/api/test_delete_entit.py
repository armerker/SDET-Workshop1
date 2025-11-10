import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from all_tests.api.models.response_models import EntityListResponse, EntityResponse
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Удаление сущности")
class TestDeleteEntity:

    @pytest.mark.api
    @allure.title("Комплексный тест удаления сущности с фикстурами")
    @allure.testcase("TC-API-005")
    def test_delete_and_verify_entity_removal(self, api_client, entity_for_deletion):
        """
        Комплексный тест с использованием фикстур:
        1. Создание сущности для удаления (через фикстуру entity_for_deletion)
        2. Удаление сущности
        3. Проверка, что сущность недоступна по ID
        4. Проверка отсутствия сущности в общем списке
        """
        entity_id = entity_for_deletion

        with allure.step("2. Удаление сущности"):
            delete_success = api_client.delete(f"delete/{entity_id}")
            assert delete_success, "Удаление сущности не удалось"

        with allure.step("3. Проверка, что сущность недоступна по ID"):
            try:
                api_client.get(f"get/{entity_id}", EntityResponse)
                assert False, "Удаленная сущность не должна быть доступна"
            except requests.exceptions.HTTPError as e:
                assert_utils.assert_status_code_in(
                    e.response.status_code,
                    [404, 400, 500],
                    "получения удаленной сущности"
                )

        with allure.step("4. Проверка отсутствия сущности в общем списке"):
            list_response = api_client.post(
                "getAll",
                EntityCreate(title="dummy"),
                EntityListResponse
            )

            entity_list = list_response.entity
            entity_ids = [entity.id for entity in entity_list]
            assert_utils.assert_not_in_list(
                entity_id,
                entity_ids,
                "в списке сущностей"
            )

        # Очистка НЕ НУЖНА - сущность уже удалена в тесте