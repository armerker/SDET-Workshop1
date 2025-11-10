import requests
import allure
from pydantic import BaseModel
from typing import Type, TypeVar, Optional, Any, Dict
from data import ApiEndpoints

T = TypeVar('T', bound=BaseModel)


class APIClient:
    """Клиент для работы с API с десериализацией в Pydantic модели"""

    def __init__(self, base_url: str = None):
        self.base_url = base_url or ApiEndpoints.BASE_URL
        self.session = requests.Session()

    @allure.step("POST запрос к {endpoint}")
    def post(self,
             endpoint: str,
             data: BaseModel,
             response_model: Type[T],
             params: Optional[Dict[str, Any]] = None) -> T:
        """
        Выполняет POST запрос с десериализацией ответа
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.post(
            url,
            json=data.model_dump(exclude_none=True),
            params=params,
            timeout=10
        )

        response.raise_for_status()

        response_data = response.json()

        if (hasattr(response_model, '__name__') and
                response_model.__name__ == "CreateEntityResponse" and
                isinstance(response_data, int)):
            return response_model(id=response_data)

        return response_model(**response_data)

    @allure.step("GET запрос к {endpoint}")
    def get(self,
            endpoint: str,
            response_model: Type[T],
            params: Optional[Dict[str, Any]] = None) -> T:
        """
        Выполняет GET запрос с десериализацией ответа
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()

        response_data = response.json()
        return response_model(**response_data)

    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint: str) -> bool:
        """
        Выполняет DELETE запрос
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.delete(url, timeout=10)
        return response.status_code == 204

    @allure.step("PATCH запрос к {endpoint}")
    def patch(self,
              endpoint: str,
              data: BaseModel,
              response_model: Type[T]) -> T:
        """
        Выполняет PATCH запрос с десериализацией ответа
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.patch(
            url,
            json=data.model_dump(exclude_none=True),
            timeout=10
        )

        response.raise_for_status()
        if response.status_code == 204 or not response.text.strip():
            if "patch" in endpoint:
                entity_id = endpoint.split("/")[-1]
                return self.get(f"get/{entity_id}", response_model)
            else:
                return response

        response_data = response.json()
        return response_model(**response_data)


api_client = APIClient()