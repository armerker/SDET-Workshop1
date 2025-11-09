import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Удаление сущности")
class TestDeleteEntity:

    def _create_test_entity(self):
        """Вспомогательный метод для создания тестовой сущности"""
        create_data = EntityCreate(
            title="Сущность для удаления",
            verified=True,
            important_numbers=[100, 200, 300]
        )
        create_response = requests.post(
            ApiEndpoints.CREATE_ENTITY,
            json=create_data.model_dump(),
            timeout=5
        )
        assert_utils.assert_status_code(
            create_response.status_code,
            200,
            "создания тестовой сущности"
        )
        return create_response.json()

    @pytest.mark.api
    @allure.title("Комплексный тест удаления сущности")
    @allure.testcase("TC-API-005")
    def test_delete_and_verify_entity_removal(self):
        """
        Комплексный тест:
        1. Создание сущности для удаления
        2. Удаление сущности
        3. Проверка, что сущность недоступна по ID
        4. Проверка отсутствия сущности в общем списке
        """
        with allure.step("1. Создание сущности для удаления"):
            entity_id = self._create_test_entity()
            assert_utils.assert_type(entity_id, int, "ID сущности")
            assert_utils.assert_positive(entity_id, "ID сущности")

        with allure.step("2. Удаление сущности"):
            delete_response = requests.delete(
                ApiEndpoints.DELETE_ENTITY.format(id=entity_id),
                timeout=5
            )

            assert_utils.assert_status_code(
                delete_response.status_code,
                204,
                "удаления сущности"
            )

        with allure.step("3. Проверка, что сущность недоступна по ID"):
            get_response = requests.get(
                ApiEndpoints.GET_ENTITY.format(id=entity_id),
                timeout=5
            )

            # Ожидаем ошибку при попытке получить удаленную сущность
            assert_utils.assert_status_code_in(
                get_response.status_code,
                [404, 400, 500],
                "получения удаленной сущности"
            )

        with allure.step("4. Проверка отсутствия сущности в общем списке"):
            list_response = requests.get(
                ApiEndpoints.GET_ALL_ENTITIES,
                timeout=5
            )

            assert_utils.assert_status_code(
                list_response.status_code,
                200,
                "получения списка сущностей"
            )

            response_data = list_response.json()
            assert_utils.assert_field_exists(response_data, "entity", "ответе API")

            # Проверяем, что удаленной сущности нет в списке
            entity_ids = [entity["id"] for entity in response_data["entity"] if "id" in entity]
            assert_utils.assert_not_in_list(
                entity_id,
                entity_ids,
                "в списке сущностей"
            )