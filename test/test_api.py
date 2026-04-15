import allure
import os
import pytest

from test.pages.yougileAPI_allure import YouGileAPI
from dotenv import load_dotenv

load_dotenv()

base_url = "https://ru.yougile.com/api-v2/"
login = os.getenv("login")
password = os.getenv("password")
companyId = "83922095-5c06-46b0-a192-0b50073ced49"
api = YouGileAPI(base_url)

keys = api.get_bearer_token(login, password, companyId)
if keys and len(keys) > 0:
    key = keys[0].get("key")
else:
    key = api.create_bearer_token(login, password, companyId)


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Позитивный тест создания проекта")
@allure.description(
    "Проверка успешного создания проекта с валидными данными и токеном"
)
def test_create_project_positive():
    """Тест создания проекта"""
    with allure.step("Создание нового проекта с названием TEST_new"):
        new_project = api.create_project("TEST_new", key)

    with allure.step("Проверка статус кода ответа"):
        assert (
            new_project.status_code == 201
        ), f"Ожидался 201, получен {new_project.status_code}"

    with allure.step("Проверка наличия ID в ответе"):
        response_json = new_project.json()
        assert "id" in response_json, "В ответе отсутствует поле id"
        allure.attach(
            f"ID созданного проекта: {response_json['id']}",
            name="Project ID",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Негативный тест создания проекта")
@allure.description("Проверка создания проекта с неверным токеном авторизации")
def test_create_project_negative():
    """Тест создания проекта с неправильным токеном"""
    with allure.step("Попытка создать проект с неверным токеном"):
        new_project = api.create_project("TEST_new", "12341234")

    with allure.step("Проверка, что получен статус код 401 (Unauthorized)"):
        assert (
            new_project.status_code == 401
        ), f"Ожидался 401, получен {new_project.status_code}"


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный тест получения проекта")
@allure.description(
    "Проверка успешного получения данных существующего проекта"
)
def test_get_project_positive():
    """Тест просмотра данных проекта"""
    with allure.step("Получение списка всех проектов"):
        projects = api.get_projects(key)
        projects_json = projects.json()

    with allure.step("Проверка наличия проектов в системе"):
        if len(projects_json.get("content", [])) > 0:
            project_info = projects_json
            project_id = project_info.get("content")[0].get("id")
            allure.attach(
                f"ID выбранного проекта: {project_id}",
                name="Project ID",
                attachment_type=allure.attachment_type.TEXT,
            )

            with allure.step(f"Получение данных проекта с ID: {project_id}"):
                project = api.get_project(project_id, key)

            with allure.step("Проверка статус кода ответа"):
                assert (
                    project.status_code == 200
                ), f"Ожидался 200, получен {project.status_code}"

            with allure.step("Проверка соответствия ID проекта"):
                assert (
                    project.json()["id"] == project_id
                ), "ID полученного проекта не совпадает с запрошенным"
        else:
            allure.attach(
                "В системе нет проектов. "
                "Для выполнения теста создайте хотя бы один проект.",
                name="Предупреждение",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.skip("Проекты не созданы! Создайте новый.")


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Негативный тест получения проекта")
@allure.description("Проверка получения проекта с несуществующим ID")
def test_get_project_negative():
    """Тест просмотра данных проекта с неправильным id проекта"""
    with allure.step("Получение списка проектов для проверки"):
        projects = api.get_projects(key)

    if len(projects.json()) > 0:
        with allure.step("Попытка получить проект с несуществующим ID '1234'"):
            project = api.get_project("1234", key)

        with allure.step("Проверка, что получен статус код 404 (Not Found)"):
            assert (
                project.status_code == 404
            ), f"Ожидался 404, получен {project.status_code}"
    else:
        allure.attach(
            "В системе нет проектов, но это не влияет на негативный тест",
            name="Информация",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный тест изменения проекта")
@allure.description(
    "Проверка успешного изменения данных существующего проекта"
)
def test_change_project_positive():
    """Тест изменения данных проекта"""
    with allure.step("Получение списка всех проектов"):
        projects = api.get_projects(key)
        projects_json = projects.json()

    with allure.step("Проверка наличия проектов для изменения"):
        if len(projects_json.get("content", [])) > 0:
            project_info = projects_json
            project_id = project_info.get("content")[0].get("id")
            allure.attach(
                f"ID выбранного проекта: {project_id}",
                name="Project ID",
                attachment_type=allure.attachment_type.TEXT,
            )

            with allure.step("Изменение названия проекта на 'NEW TEST3'"):
                project = api.change_project(
                    project_id, key, title="NEW TEST3"
                )

            with allure.step("Проверка статус кода ответа"):
                assert (
                    project.status_code == 200
                ), f"Ожидался 200, получен {project.status_code}"

            with allure.step("Проверка, что ID проекта не изменился"):
                assert (
                    project.json()["id"] == project_id
                ), "ID проекта изменился после обновления"

            with allure.step(
                "Дополнительная проверка: получение обновленного проекта"
            ):
                updated_project = api.get_project(project_id, key)
                assert updated_project.status_code == 200
                allure.attach(
                    f"Новое название проекта: "
                    f"{updated_project.json().get('title')}",
                    name="Updated Title",
                    attachment_type=allure.attachment_type.TEXT,
                )
        else:
            allure.attach(
                "В системе нет проектов. "
                "Для выполнения теста создайте хотя бы один проект.",
                name="Предупреждение",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.skip("Проекты не созданы! Создайте новый.")


@allure.feature("Проекты YouGile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Негативный тест изменения проекта")
@allure.description(
    "Проверка изменения проекта с неверным токеном авторизации"
)
def test_change_project_negative():
    """Тест изменения данных проекта с неправильным токеном"""
    with allure.step("Получение списка проектов"):
        projects = api.get_projects(key)

    if len(projects.json()) > 0:
        project_info = projects.json()
        project_id = project_info.get("content")[0].get("id")
        allure.attach(
            f"ID выбранного проекта: {project_id}",
            name="Project ID",
            attachment_type=allure.attachment_type.TEXT,
        )

        with allure.step("Попытка изменить проект с неверным токеном"):
            project = api.change_project(project_id, "123", title="NEW TEST3")

        with allure.step(
            "Проверка, что получен статус код 401 (Unauthorized)"
        ):
            assert (
                project.status_code == 401
            ), f"Ожидался 401, получен {project.status_code}"
    else:
        allure.attach(
            "В системе нет проектов, но это не влияет на негативный тест",
            name="Информация",
            attachment_type=allure.attachment_type.TEXT,
        )
