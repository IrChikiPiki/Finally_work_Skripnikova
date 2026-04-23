from config_manager import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import os
from dotenv import load_dotenv
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

load_dotenv()


class LoginYouGilePage:
    """Класс главной страницы YuoGile"""

    def __init__(self, driver) -> None:
        """Метод инициализации класса"""
        self.driver = driver
        self.log = os.getenv("login")
        self.password = os.getenv("password")
        self.driver.get(f"{os.getenv("url")}")
        self.wait = WebDriverWait(driver, 30)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)

    def login(self) -> None:
        """Метод авторизации в системе"""
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='email']")
            )
        )
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='email']"
        ).send_keys(f"{self.log}")
        self.driver.find_element(
            By.CSS_SELECTOR, "input[type='password']"
        ).send_keys(f"{self.password}")
        self.driver.find_element(By.CSS_SELECTOR, "div[role='button']").click()


class MainYouGilePage:
    """Класс основной страницы YouGile"""

    def __init__(self, driver) -> None:
        """Метод инициализации класса"""
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.task_name = config.ui.task_name

    def create_task(self, task_title: str) -> str:
        """Создает задачу и возвращает фактическое имя созданной карточки.
        Args:
            task_title: Название создаваемой задачи.
        Returns:
            str: Название созданной задачи.
        """
        target_task_title: str = task_title

        # Добавление задач
        button = (self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'truncate') "
                    f"and text()='{config.projects.main_project}']",
                )
            )
        ))
        button.click()
        button_2 = (self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//span[text()='{config.projects.column_name}']/ancestor::"
                    "div[contains(@class, 'task-group-title-new')]"
                    "//span[text()='Добавить задачу']",
                )
            )
        ))
        button_2.click()
        self.driver.find_element(
            By.XPATH, "//textarea[@placeholder='Введите название задачи…']"
        ).send_keys(target_task_title)
        self.actions.send_keys(Keys.ENTER).perform()
        return target_task_title

    def get_task_name(self, task_title: str | None = None) -> str:
        """Возвращает название задачи по ожидаемому имени.

        Args:
            task_title: Название задачи для поиска. Если не передано,
                используется значение из конфигурации.

        Returns:
            str: Текст заголовка найденной задачи.
        """
        target_task_title: str = task_title or self.task_name
        created_task = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@data-testid='board-task-card']"
                    f"//span[text()='{target_task_title}']",
                )
            )
        )
        return created_task.text

    def assign_performer(self, task_title: str | None = None) -> None:
        """Назначает исполнителя задаче с указанным названием.

        Args:
            task_title: Название задачи, в которую нужно назначить исполнителя.
                Если не передано, используется значение из конфигурации.
        """
        target_task_title: str = task_title or self.task_name
        task = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[@data-testid='board-task-card']"
                    f"[.//span[text()='{target_task_title}']]",
                )
            )
        )
        self.actions.move_to_element(task).perform()
        task.find_element(By.CSS_SELECTOR, "[data-testid='board-user-sticker']").click()
        performer_option = (self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{config.ui.performer_name}']")
            )
        ))
        performer_option.click()
        self.actions.send_keys(Keys.ESCAPE).perform()

    def get_performer_name(self, task_title: str | None = None) -> str:
        """Возвращает отображаемое имя исполнителя у выбранной задачи.

        Args:
            task_title: Название задачи, у которой нужно прочитать исполнителя.
                Если не передано, используется значение из конфигурации.

        Returns:
            str: Отображаемое сокращенное имя исполнителя на карточке.
        """
        target_task_title: str = task_title or self.task_name
        task_with_executor = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@data-testid='board-task-card']"
                    f"[.//span[text()='{target_task_title}']]"
                    f"//div[@class='user-avatar sticker-item-icon']",
                )
            )
        )
        return task_with_executor.text

    def transfer_task(self, task_title: str | None = None) -> None:
        """Перемещает выбранную задачу в целевую колонку.

        Args:
            task_title: Название задачи, которую нужно переместить.
                Если не передано, используется значение из конфигурации.
        """
        target_task_title: str = task_title or self.task_name
        task = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//span[text()='{target_task_title}']"
                    f"/ancestor::div[@data-testid='board-task-card']",
                )
            )
        )
        self.actions.move_to_element(task).perform()
        task.find_element(By.CSS_SELECTOR, "[data-testid='board-task-menu']").click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'group/menu-item')]"
                    "//div[text()='Переместить']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[text()='Указать место назначения...']")
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@class='ml-4 flex-1 text-no-wrap' "
                    f"and text()='{config.projects.main_project}']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'text-no-wrap') "
                    f"and text()='{config.projects.board_name}']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'text-no-wrap') "
                    f"and text()='{config.projects.target_column}']",
                )
            )
        ).click()
        sleep(2)

    def delete_task(self, task_title: str | None = None) -> None:
        """Удаляет задачу по указанному названию.

        Args:
            task_title: Название задачи для удаления.
                Если не передано, используется значение из конфигурации.
        """
        target_task_title: str = task_title or self.task_name
        menu_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@data-testid='board-task-card']"
                    f"[.//span[text()='{target_task_title}']]"
                    "//div[@data-testid='board-task-menu']",
                )
            )
        )
        menu_button.click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Удалить']"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button']//div[text()='Удалить']")
            )
        ).click()
