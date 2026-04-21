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

    def create_task(self) -> None:
        """Метод создание задачи"""
        # Добавление задач
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'truncate') "
                    f"and text()='{config.projects.main_project}']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//span[text()='{config.projects.column_name}']/ancestor::"
                    "div[contains(@class, 'task-group-title-new')]"
                    "//span[text()='Добавить задачу']",
                )
            )
        ).click()
        self.driver.find_element(
            By.XPATH, "//textarea[@placeholder='Введите название задачи…']"
        ).send_keys(f"{self.task_name}")
        # actions = ActionChains(self.driver)
        self.actions.send_keys(Keys.ENTER).perform()

    def get_task_name(self) -> str:
        """Метод получения имени созданной задачи"""
        created_task = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@data-testid='board-task-card']"
                    f"//span[text()='{self.task_name}']",
                )
            )
        )
        return created_task.text

    def assign_performer(self) -> None:
        """Метод назначения исполнителя задачи"""
        task = self.driver.find_element(
            By.CSS_SELECTOR, "[data-testid='board-task-card']"
        )
        self.actions.move_to_element(task).perform()
        self.driver.find_element(
            By.CSS_SELECTOR, "[data-testid='board-user-sticker']"
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{config.ui.performer_name}']")
            )
        ).click()
        self.actions.send_keys(Keys.ESCAPE).perform()

    def get_performer_name(self) -> str:
        """Метод получения имени исполнителя задачи"""
        task_with_executor = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//div[@data-testid='board-task-card']"
                    f"[.//span[text()='{self.task_name}']]"
                    f"//div[@class='user-avatar sticker-item-icon']",
                )
            )
        )
        return task_with_executor.text

    def transfer_task(self) -> None:
        """Метод переноса задачи"""
        task = self.driver.find_element(
            By.XPATH,
            f"//span[text()='{self.task_name}']"
            f"/ancestor::div[@data-testid='board-task-card']",
        )
        self.actions.move_to_element(task).perform()
        self.driver.find_element(
            By.CSS_SELECTOR, "[data-testid='board-task-menu']"
        ).click()
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

    def delete_task(self) -> None:
        """Метод удаления задачи"""
        menu_button = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[@data-testid='tw-task-container']"
                    "[.//span[text()='Тестовая задача']]"
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
