import pytest
import allure
from all_tests.api.models.entity_model import EntityCreate
from all_tests.api.models.response_models import EntityResponse, EntityListResponse
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Получение всех сущностей")
class TestGetAllEntities:

    @pytest.mark.api
    @allure.title("Комплексный тест получения всех сущностей")
    @allure.testcase("TC-API-003")
    def test_get_all_entities_with_data_verification(self, api_client, multiple_test_entities):
        """
        Предусловия:
        - Созданы тестовые сущности (через фикстуру multiple_test_entities)

        Шаги:
        1. Получить общий список сущностей через POST
        2. Проверить структуру ответа
        3. Проверить наличие созданных сущностей в списке
        4. Проверить структуру элементов списка

        Постусловия:
        - Удалить тестовые данные (автоматически через фикстуру)
        """
        # Фикстура multiple_test_entities УЖЕ создала сущности на шаге 1
        created_ids = multiple_test_entities
        test_entity_id = created_ids[0]

        with allure.step("1. Получение и проверка общего списка сущностей через POST"):
            response = api_client.post(
                "getAll",
                EntityCreate(title="dummy"),
                EntityListResponse
            )

            assert hasattr(response, "entity"), "Поле 'entity' отсутствует в ответе"
            assert_utils.assert_type(response.entity, list, "поле entity")

        with allure.step("2. Проверка структуры ответа"):
            entity_list = response.entity

            assert_utils.assert_type(entity_list, list, "список сущностей")

            if entity_list:
                entity_ids = [entity.id for entity in entity_list]
                assert_utils.assert_in_list(test_entity_id, entity_ids, "в списке сущностей")

        with allure.step("3. Проверка структуры элементов списка"):
            if entity_list:
                sample_entity = entity_list[0]
                expected_fields = ["id", "title"]

                for field in expected_fields:
                    assert hasattr(sample_entity, field), f"Поле {field} отсутствует"

                assert_utils.assert_type(sample_entity.id, int, "id")
                assert_utils.assert_type(sample_entity.title, str, "title")

        # Очистка АВТОМАТИЧЕСКАЯ через фикстуру multiple_test_entities