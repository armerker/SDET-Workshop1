import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate
from data import ApiEndpoints
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Получение всех сущностей")
class TestGetAllEntities:

    @pytest.mark.api
    @allure.title("Комплексный тест получения всех сущностей")
    @allure.testcase("TC-API-003")
    def test_get_all_entities_with_data_verification(self):
        """
        Комплексный тест:
        1. Создание тестовой сущности
        2. Получение общего списка через POST
        3. Проверка структуры и данных
        """
        with allure.step("1. Создание тестовой сущности для проверки списка"):
            create_data = EntityCreate(
                title="Тест для проверки общего списка",
                verified=False,
                important_numbers=[10, 20, 30]
            )

            create_response = requests.post(
                ApiEndpoints.CREATE_ENTITY,
                json=create_data.model_dump(),
                timeout=5
            )

            assert_utils.assert_status_code(create_response.status_code, 200, "создания")
            test_entity_id = create_response.json()
            assert_utils.assert_type(test_entity_id, int, "ID")
            assert_utils.assert_positive(test_entity_id, "ID")

        with allure.step("2. Получение и проверка общего списка сущностей через POST"):
            # ИСПРАВЛЕНО: POST запрос для getAll
            response = requests.post(ApiEndpoints.GET_ALL_ENTITIES, timeout=5)

            assert_utils.assert_status_code(response.status_code, 200, "получения списка")

            response_data = response.json()
            assert_utils.assert_type(response_data, dict, "ответа")  # Теперь dict, а не list
            assert_utils.assert_field_exists(response_data, "entity", "ответе")
            assert_utils.assert_type(response_data["entity"], list, "поле entity")

        with allure.step("3. Проверка наличия тестовой сущности в списке"):
            entity_list = response_data["entity"]
            entity_ids = [entity["id"] for entity in entity_list if "id" in entity]
            assert_utils.assert_in_list(test_entity_id, entity_ids, "в списке сущностей")

        with allure.step("4. Проверка структуры элементов списка"):
            if entity_list:
                sample_entity = entity_list[0]
                expected_fields = ["id", "title"]
                assert_utils.assert_api_response_structure(sample_entity, expected_fields)

                assert_utils.assert_type(sample_entity["id"], int, "id")
                assert_utils.assert_type(sample_entity["title"], str, "title")