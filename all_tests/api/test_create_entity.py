import pytest
import allure
import requests
from all_tests.api.models.entity_models import EntityCreate, AdditionRequest
from data import ApiEndpoints, ApiTestData
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Создание и проверка сущности")
class TestCreateEntity:

    @pytest.mark.api
    @allure.title("Комплексный тест создания и проверки сущности")
    @allure.testcase("TC-API-001")
    def test_create_and_verify_entity(self):
        """
        Комплексный тест:
        1. Создание сущности
        2. Проверка получения по ID
        3. Проверка наличия в общем списке
        """
        with allure.step("1. Создание сущности"):
            entity_data = EntityCreate(
                title="Тестовая сущность для проверки",
                verified=True,
                important_numbers=[42, 87, 15],
                addition=AdditionRequest(
                    additional_info="Дополнительные сведения",
                    additional_number=123
                )
            )

            create_response = requests.post(
                ApiEndpoints.CREATE_ENTITY,
                json=entity_data.model_dump(),
                timeout=5
            )

            assert_utils.assert_status_code(
                create_response.status_code,
                200,
                "создания сущности"
            )

            created_id = create_response.json()
            assert_utils.assert_type(created_id, int, "ID сущности")
            assert_utils.assert_positive(created_id, "ID сущности")

        with allure.step("2. Проверка получения сущности по ID"):
            get_response = requests.get(
                ApiEndpoints.GET_ENTITY.format(id=str(created_id)),  # ID как string
                timeout=5
            )

            assert_utils.assert_status_code(
                get_response.status_code,
                200,
                "получения сущности по ID"
            )

            retrieved_entity = get_response.json()
            assert_utils.assert_equal(
                retrieved_entity["id"],
                created_id,
                "ID сущности"
            )
            assert_utils.assert_equal(
                retrieved_entity["title"],
                entity_data.title,
                "title"
            )
            assert_utils.assert_equal(
                retrieved_entity["verified"],
                entity_data.verified,
                "verified"
            )

        with allure.step("3. Проверка наличия сущности в общем списке"):
            # ИСПРАВЛЕНО: POST запрос для getAll
            list_response = requests.post(
                ApiEndpoints.GET_ALL_ENTITIES,
                timeout=5
            )

            assert_utils.assert_status_code(
                list_response.status_code,
                200,
                "получения списка сущностей"
            )

            response_data = list_response.json()
            assert_utils.assert_type(response_data, dict, "ответ API")
            assert_utils.assert_field_exists(response_data, "entity", "ответе API")
            assert_utils.assert_type(response_data["entity"], list, "поле entity")

            # Проверяем, что созданная сущность есть в списке
            entity_list = response_data["entity"]
            entity_ids = [entity["id"] for entity in entity_list if "id" in entity]
            assert_utils.assert_in_list(
                created_id,
                entity_ids,
                "в списке сущностей"
            )