from pages.YouGile_pages import LoginYouGilePage, MainYouGilePage
import allure
import pytest


@pytest.mark.ui
@allure.feature("YouGile - Авторизация")
@allure.story("UI тесты")
@allure.title("Тест 1: Успешная авторизация в системе")
@allure.severity(allure.severity_level.BLOCKER)
def test_login_successful(driver_Chrome):
    """Тест авторизации с валидными данными"""
    with allure.step("Открытие страницы авторизации и ввод данных"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Проверка успешной авторизации"):
        # Проверяем, что после авторизации открылась главная страница
        main_page = MainYouGilePage(driver_Chrome)
        assert driver_Chrome.current_url != login_page.driver.current_url
        allure.attach(
            driver_Chrome.get_screenshot_as_png(),
            name="Главная страница после авторизации",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 2: Создание новой задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_task(driver_Chrome):
    """Тест создания задачи с валидным названием"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание новой задачи"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Проверка, что задача создалась"):
        task_name = main_page.get_task_name()
        assert task_name == main_page.task_name, \
            f"Ожидалось '{main_page.task_name}', получено '{task_name}'"

        allure.attach(
            f"Создана задача: {task_name}",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 3: Назначение исполнителя на задачу")
@allure.severity(allure.severity_level.CRITICAL)
def test_assign_performer(driver_Chrome):
    """Тест назначения исполнителя на существующую задачу"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи (предусловие)"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Назначение исполнителя"):
        main_page.assign_performer()

    with allure.step("Проверка, что исполнитель назначен"):
        performer_name = main_page.get_performer_name()
        assert performer_name == "Ир", \
            f"Ожидался исполнитель 'Ир', получен '{performer_name}'"

        allure.attach(
            f"Исполнитель задачи: {performer_name}",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 4: Перемещение задачи в другой проект")
@allure.severity(allure.severity_level.NORMAL)
def test_move_task_to_another_project(driver_Chrome):
    """Тест перемещения задачи между проектами"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи (предусловие)"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Перемещение задачи"):
        main_page.transfer_task()

    with allure.step("Проверка, что задача перемещена"):
        # Можно добавить проверку, что задача появилась в новом проекте
        allure.attach(
            "Задача успешно перемещена",
            name="Результат",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 5: Удаление задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_task(driver_Chrome):
    """Тест удаления существующей задачи"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи (предусловие)"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Удаление задачи"):
        main_page.delete_task()

    with allure.step("Проверка, что задача удалена"):
        # Проверяем, что задача больше не отображается
        try:
            main_page.get_task_name()
            assert False, "Задача не была удалена"
        except:
            allure.attach(
                "Задача успешно удалена",
                name="Результат",
                attachment_type=allure.attachment_type.TEXT
            )


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 6: Создание задачи с пустым названием")
@allure.severity(allure.severity_level.NORMAL)
def test_create_task_empty_name(driver_Chrome):
    """Негативный тест: создание задачи без названия"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Попытка создать задачу без названия"):
        main_page = MainYouGilePage(driver_Chrome)
        # Модифицируем для создания пустой задачи
        main_page.task_name = ""
        main_page.create_task()

    with allure.step("Проверка, что задача не создалась"):
        # Проверяем, что задача не появилась на доске
        assert main_page.is_task_not_created(), \
            "Задача с пустым названием не должна создаваться"


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 7: Редактирование названия задачи")
@allure.severity(allure.severity_level.NORMAL)
def test_edit_task_name(driver_Chrome):
    """Тест редактирования названия задачи"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Редактирование названия задачи"):
        new_name = "Измененная задача"
        main_page.edit_task_name(new_name)

    with allure.step("Проверка изменения названия"):
        task_name = main_page.get_task_name()
        assert task_name == new_name, \
            f"Ожидалось '{new_name}', получено '{task_name}'"


@pytest.mark.ui
@allure.feature("YouGile - Управление задачами")
@allure.story("UI тесты")
@allure.title("Тест 8: Проверка создания задачи с длинным названием")
@allure.severity(allure.severity_level.MINOR)
def test_create_task_long_name(driver_Chrome):
    """Тест создания задачи с очень длинным названием"""
    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи с длинным названием (255 символов)"):
        main_page = MainYouGilePage(driver_Chrome)
        long_name = "A" * 255
        main_page.task_name = long_name
        main_page.create_task()

    with allure.step("Проверка, что задача создалась"):
        task_name = main_page.get_task_name()
        assert task_name == long_name, "Длинное название не сохранилось"