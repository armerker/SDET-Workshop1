from faker import Faker
from typing import List, Optional
from all_tests.api.models.entity_model import EntityCreate, EntityUpdate, AdditionRequest


class DataGenerator:
    """Генератор случайных тестовых данных для API"""

    def __init__(self, locale: str = "ru_RU"):
        self.fake = Faker(locale)

    def generate_entity_create_data(self,
                                    title: Optional[str] = None,
                                    verified: Optional[bool] = None,
                                    with_addition: bool = True) -> EntityCreate:
        """
        Генерирует случайные данные для создания сущности

        Args:
            title: Конкретный заголовок (если None - генерируется случайный)
            verified: Статус verified (если None - случайный)
            with_addition: Добавлять ли дополнительную информацию

        Returns:
            EntityCreate: Данные для создания сущности
        """
        return EntityCreate(
            title=title or self.fake.sentence(nb_words=3).rstrip('.'),
            verified=verified if verified is not None else self.fake.boolean(),
            important_numbers=[self.fake.random_int(1, 100) for _ in range(3)],
            addition=self.generate_addition_data() if with_addition else None
        )

    def generate_entity_update_data(self,
                                    title: Optional[str] = None,
                                    verified: Optional[bool] = None) -> EntityUpdate:
        """
        Генерирует случайные данные для обновления сущности

        Returns:
            EntityUpdate: Данные для обновления сущности
        """
        return EntityUpdate(
            title=title or f"Обновленный {self.fake.sentence(nb_words=2).rstrip('.')}",
            verified=verified if verified is not None else self.fake.boolean(),
            important_numbers=[self.fake.random_int(50, 200) for _ in range(2)],
            addition=self.generate_addition_data()
        )

    def generate_addition_data(self) -> AdditionRequest:
        """
        Генерирует случайные данные для дополнительной информации

        Returns:
            AdditionRequest: Данные дополнительной информации
        """
        return AdditionRequest(
            additional_info=self.fake.text(max_nb_chars=100),
            additional_number=self.fake.random_int(1, 1000)
        )

    def generate_multiple_entities(self, count: int = 3) -> List[EntityCreate]:
        """
        Генерирует несколько наборов данных для создания сущностей

        Args:
            count: Количество сущностей для генерации

        Returns:
            List[EntityCreate]: Список данных для создания сущностей
        """
        return [self.generate_entity_create_data() for _ in range(count)]

    def get_test_cases(self) -> dict:
        """
        Возвращает набор тестовых случаев для разных сценариев

        Returns:
            dict: Словарь с тестовыми данными
        """
        return {
            "simple_entity": self.generate_entity_create_data(
                title="Простая сущность",
                verified=True,
                with_addition=False
            ),
            "entity_with_addition": self.generate_entity_create_data(
                title="Сущность с дополнением",
                verified=False,
                with_addition=True
            ),
            "long_title": self.generate_entity_create_data(
                title=self.fake.sentence(nb_words=10),
                verified=True
            ),
            "special_chars": self.generate_entity_create_data(
                title="Сущность с спец-символами !@#$%^&*()",
                verified=False
            )
        }

data_generator = DataGenerator()