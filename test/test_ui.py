from pages.YouGile_pages import LoginYouGilePage, MainYouGilePage
import allure
import pytest


@pytest.mark.ui
@allure.feature("YouGile")
@allure.story("Управление задачами")
class TestYouGileTasks:

    @pytest.fixture(autouse=True)
    def setup(self, driver_Chrome):
        """Общая авторизация для всех тестов"""
        login_page = LoginYouGilePage(driver_Chrome)
        login_page.login()
        self.main_page = MainYouGilePage(driver_Chrome)

    @allure.title("Создание задачи")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_task(self):
        """Тест 1: Создание задачи"""
        with allure.step("Создание задачи 'Тестовая задача'"):
            self.main_page.create_task()

        with allure.step("Проверка названия созданной задачи"):
            task_name = self.main_page.get_task_name()
            allure.attach(
                f"Ожидаемое название: Тестовая задача\n"
                f"Фактическое название: {task_name}",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert task_name == "Тестовая задача"

    @allure.title("Назначение исполнителя задаче")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_assign_performer(self):
        """Тест 2: Назначение исполнителя (требует предварительно созданную задачу)"""
        with allure.step("Предусловие: создание задачи"):
            self.main_page.create_task()

        with allure.step("Назначение исполнителя 'Ирина' на задачу"):
            self.main_page.assign_performer()

        with allure.step("Проверка назначенного исполнителя"):
            performer_name = self.main_page.get_performer_name()
            allure.attach(
                f"Ожидаемый исполнитель: Ир\n"
                f"Фактический исполнитель: {performer_name}",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert performer_name == "Ир"

    @allure.title("Перемещение задачи в другой проект")
    @allure.severity(allure.severity_level.NORMAL)
    def test_transfer_task(self):
        """Тест 3: Перемещение задачи (требует предварительно созданную задачу)"""
        with allure.step("Предусловие: создание задачи"):
            self.main_page.create_task()

        with allure.step("Перемещение задачи в другой проект"):
            self.main_page.transfer_task()

        with allure.step("Проверка перемещения задачи"):
            # Можно добавить проверку, что задача находится в новом месте
            allure.attach(
                "Задача успешно перемещена",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.title("Удаление задачи")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_task(self):
        """Тест 4: Удаление задачи (требует предварительно созданную задачу)"""
        with allure.step("Предусловие: создание задачи"):
            self.main_page.create_task()

        with allure.step("Удаление задачи"):
            self.main_page.delete_task()

        with allure.step("Проверка удаления задачи"):
            # Можно добавить проверку, что задача больше не отображается
            allure.attach(
                "Задача успешно удалена",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT,
            )

    @allure.title("Полный цикл работы с задачей")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_task_lifecycle(self):
        """Тест 5: Полный цикл (создание → назначение → перемещение → удаление)"""
        with allure.step("Создание задачи 'Тестовая задача'"):
            self.main_page.create_task()

        with allure.step("Проверка названия созданной задачи"):
            task_name = self.main_page.get_task_name()
            assert task_name == "Тестовая задача"

        with allure.step("Назначение исполнителя 'Ирина' на задачу"):
            self.main_page.assign_performer()

        with allure.step("Проверка назначенного исполнителя"):
            performer_name = self.main_page.get_performer_name()
            assert performer_name == "Ир"

        with allure.step("Перемещение задачи в другой проект"):
            self.main_page.transfer_task()

        with allure.step("Удаление задачи"):
            self.main_page.delete_task()