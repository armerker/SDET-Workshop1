import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Получение сущности по ID")
class TestGetEntity:

    @pytest.mark.api
    @allure.title("Комплексный тест получения сущности по ID")
    @allure.testcase("TC-API-002")
    def test_create_and_get_entity_by_id(self):
        """
        Комплексный тест:
        1. Создание сущности
        2. Получение по ID и проверка данных
        3. Проверка в общем списке
        """
        with allure.step("1. Создание тестовой сущности"):
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

            assert_utils.assert_status_code(create_response.status_code, 200, "создания")
            created_id = create_response.json()
            assert_utils.assert_type(created_id, int, "ID")
            assert_utils.assert_positive(created_id, "ID")

        with allure.step("2. Получение сущности по ID"):
            get_response = requests.get(
                ApiEndpoints.GET_ENTITY.format(id=str(created_id)),  # ID как string
                timeout=5
            )

            assert_utils.assert_status_code(get_response.status_code, 200, "получения по ID")

            retrieved_entity = get_response.json()
            assert_utils.assert_equal(retrieved_entity["id"], created_id, "ID")
            assert_utils.assert_equal(retrieved_entity["title"], create_data.title, "title")
            assert_utils.assert_equal(retrieved_entity["verified"], create_data.verified, "verified")

        with allure.step("3. Проверка в общем списке"):
            # ИСПРАВЛЕНО: POST запрос для getAll
            list_response = requests.post(ApiEndpoints.GET_ALL_ENTITIES, timeout=5)
            assert_utils.assert_status_code(list_response.status_code, 200, "получения списка")

            response_data = list_response.json()
            assert_utils.assert_field_exists(response_data, "entity", "ответе")

            entity_list = response_data["entity"]
            entity_ids = [entity["id"] for entity in entity_list if "id" in entity]
            assert_utils.assert_in_list(created_id, entity_ids, "в списке")