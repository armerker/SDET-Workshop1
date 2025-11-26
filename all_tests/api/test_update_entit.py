import pytest
import allure
from all_tests.api.models.entity_model import EntityUpdate, AdditionRequest
from all_tests.api.models.response_models import EntityResponse
from all_tests.api.utils.assert_utils import assert_utils


@allure.feature("API Entity Management")
@allure.story("Обновление сущности")
class TestUpdateEntity:

    @pytest.mark.api
    @allure.title("Комплексный тест обновления сущности с фикстурами")
    @allure.testcase("TC-API-004")
    def test_update_and_verify_entity(self, api_client, entity_for_update):
        """
        Предусловия:
        - Создана тестовая сущность для обновления (через фикстуру entity_for_update)

        Шаги:
        1. Обновить сущность
        2. Проверить обновленные данные
        3. Проверить сохранение изменений при повторном получении

        Постусловия:
        - Удалить тестовые данные (автоматически через фикстуру)
        """
        entity_id = entity_for_update

        with allure.step("1. Обновление сущности"):
            update_data = EntityUpdate(
                title="Обновленное название",
                verified=True,
                important_numbers=[99, 88, 77],
                addition=AdditionRequest(
                    additional_info="Новая дополнительная информация",
                    additional_number=999
                )
            )

            updated_entity = api_client.patch(
                f"patch/{entity_id}",
                update_data,
                EntityResponse
            )

            assert_utils.assert_equal(updated_entity.id, entity_id, "ID после обновления")
            assert_utils.assert_equal(updated_entity.title, update_data.title, "title после обновления")
            assert_utils.assert_equal(updated_entity.verified, update_data.verified, "verified после обновления")

        with allure.step("2. Проверка что обновления сохранились при повторном получении"):
            retrieved_entity = api_client.get(
                f"get/{entity_id}",
                EntityResponse
            )

            assert_utils.assert_equal(retrieved_entity.title, update_data.title, "title при повторном получении")
            assert_utils.assert_equal(retrieved_entity.verified, update_data.verified,
                                      "verified при повторном получении")

        # Очистка АВТОМАТИЧЕСКАЯ через фикстуру entity_for_update