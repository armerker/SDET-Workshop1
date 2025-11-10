import pytest
import allure
from all_tests.api.models.entity_model import EntityCreate
from all_tests.api.models.response_models import EntityResponse, EntityListResponse
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Создание и проверка сущности")
class TestCreateEntity:

    @pytest.mark.api
    @allure.title("Комплексный тест создания и проверки сущности")
    @allure.testcase("TC-API-001")
    def test_create_and_verify_entity(self, api_client, test_entity):
        """
        Комплексный тест с использованием фикстур:
        1. Создание сущности (через фикстуру test_entity)
        2. Проверка получения по ID
        3. Проверка наличия в общем списке
        """
        entity_id = test_entity

        with allure.step("2. Проверка получения сущности по ID"):
            retrieved_entity = api_client.get(
                f"get/{entity_id}",
                EntityResponse
            )

            assert_utils.assert_equal(
                retrieved_entity.id,
                entity_id,
                "ID сущности"
            )
            assert_utils.assert_type(retrieved_entity.title, str, "title")

        with allure.step("3. Проверка наличия сущности в общем списке"):
            list_response = api_client.post(
                "getAll",
                EntityCreate(title="dummy"),
                EntityListResponse
            )

            entity_list = list_response.entity
            assert_utils.assert_type(entity_list, list, "список сущностей")

            # Если список не пустой - проверяем наличие нашей сущности
            if entity_list:
                entity_ids = [entity.id for entity in entity_list]
                assert_utils.assert_in_list(
                    entity_id,
                    entity_ids,
                    "в списке сущностей"
                )

        # Очистка АВТОМАТИЧЕСКАЯ через фикстуру test_entity