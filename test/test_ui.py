from .pages.YouGile_pages import LoginYouGilePage, MainYouGilePage
import allure


@allure.feature("YouGile")
@allure.story("Управление задачами")
@allure.title("Создание, назначение исполнителя, перемещение и удаление задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_YouGile(driver_Chrome):
    """Тестирование YouGile: полный цикл работы с задачей"""

    with allure.step("Авторизация в системе"):
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()

    with allure.step("Создание задачи 'Тестовая задача'"):
        main_page = MainYouGilePage(driver_Chrome)
        main_page.create_task()

    with allure.step("Проверка названия созданной задачи"):
        task_name = main_page.get_task_name()
        allure.attach(
            f"Ожидаемое название: Тестовая задача\nФактическое название: {task_name}",
            name="Результат проверки",
            attachment_type=allure.attachment_type.TEXT
        )
        assert task_name == "Тестовая задача"

    with allure.step("Назначение исполнителя 'Ирина' на задачу"):
        main_page.assign_performer()

    with allure.step("Проверка назначенного исполнителя"):
        performer_name = main_page.get_performer_name()
        allure.attach(
            f"Ожидаемый исполнитель: Ир\nФактический исполнитель: {performer_name}",
            name="Результат проверки",
            attachment_type=allure.attachment_type.TEXT
        )
        assert performer_name == "Ир"

    with allure.step("Перемещение задачи в другой проект"):
        main_page.transfer_task()

    with allure.step("Удаление задачи"):
        main_page.delete_task()
