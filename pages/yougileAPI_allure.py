from config_manager import config
import requests
from typing import Optional, Dict, List, Any


class YouGileAPI:
    """Класс для работы с API YouGile"""

    def __init__(self, url: str) -> None:
        """
        Инициализация API клиента

        Args:
            url: Базовый URL API YouGile
        """
        self.url = url

    def create_bearer_token(
        self, login: str, password: str, companyId: str
    ) -> Optional[str]:
        """
        Создание токена авторизации

        Args:
            login: логин от аккаунта в YouGile
            password: пароль от аккаунта в YouGile
            companyId: id компании в YouGile

        Returns:
            Токен авторизации или None в случае ошибки
        """
        auth: Dict[str, str] = {
            "login": login,
            "password": password,
            "companyId": companyId,
        }
        try:
            resp = requests.post(self.url + "auth/keys", json=auth)
            resp.raise_for_status()
            return resp.json().get("key")
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Ошибка при создании токена: {e}")
            return None

    def get_bearer_token(
        self, login: str, password: str, companyId: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Получение списка токенов авторизации

        Args:
            login: логин от аккаунта в YouGile
            password: пароль от аккаунта в YouGile
            companyId: id компании в YouGile

        Returns:
            Список токенов авторизации или None в случае ошибки
        """
        auth: Dict[str, str] = {
            "login": login,
            "password": password,
            "companyId": companyId,
        }
        try:
            resp = requests.post(self.url + "auth/keys/get", json=auth)
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Ошибка при получении токенов: {e}")
            return None

    def create_project(
        self, project_name: str, token: str
    ) -> requests.Response:
        """
        Создание проекта

        Args:
            project_name: название нового проекта в YouGile
            token: токен авторизации в YouGile

        Returns:
            Response объект с результатом создания проекта
        """
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload: Dict[str, str] = {
            "title": project_name,
        }
        new_project = requests.post(
            self.url + "projects", json=payload, headers=headers
        )
        return new_project

    def get_project(self, project_id: str, token: str) -> requests.Response:
        """
        Получение данных проекта

        Args:
            project_id: id проекта в YouGile
            token: токен авторизации в YouGile

        Returns:
            Response объект с данными проекта
        """
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        resp = requests.get(
            self.url + f"projects/{project_id}", headers=headers
        )
        return resp

    def get_projects(self, token: str) -> requests.Response:
        """
        Получение списка проектов

        Args:
            token: токен авторизации в YouGile

        Returns:
            Response объект со списком проектов
        """
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        resp = requests.get(self.url + "projects", headers=headers)
        return resp

    def change_project(
        self,
        project_id: str,
        token: str,
        title: str = "Пример проекта",
        deleted: bool = False,
    ) -> requests.Response:
        """
        Изменение данных проекта

        Args:
            project_id: id проекта в YouGile
            token: токен авторизации в YouGile
            title: имя проекта
            deleted: статус удаления

        Returns:
            Response объект с результатом изменения
        """
        payload: Dict[str, Any] = {
            "deleted": deleted,
            "title": title,
            "users": {
                config.api.user_id: "admin",
            },
        }
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        resp = requests.put(
            self.url + f"projects/{project_id}", json=payload, headers=headers
        )
        return resp
