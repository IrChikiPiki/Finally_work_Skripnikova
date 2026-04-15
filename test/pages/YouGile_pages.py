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
    """Класс главной страницы магазина одежды"""

    def __init__(self, driver):
        self.driver = driver
        self.log = os.getenv("login")
        self.password = os.getenv("password")
        self.driver.get(f"{os.getenv("url")}")
        self.wait = WebDriverWait(driver, 15)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)

    def login(self):
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
    """Класс страницы с карточками товаров магазина одежды"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.driver.maximize_window()
        self.actions = ActionChains(self.driver)
        self.task_name = "Тестовая задача"

    def create_task(self):
        # Добавление задач
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'truncate') "
                    "and text()='FINALLY_PROJ']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[text()='SkripnikovaFINAL_2']/ancestor::"
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

    def get_task_name(self):
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

    def assign_performer(self):
        task = self.driver.find_element(
            By.CSS_SELECTOR, "[data-testid='board-task-card']"
        )
        self.actions.move_to_element(task).perform()
        self.driver.find_element(
            By.CSS_SELECTOR, "[data-testid='board-user-sticker']"
        ).click()
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Ирина']"))
        ).click()
        self.actions.send_keys(Keys.ESCAPE).perform()

    def get_performer_name(self):
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

    def transfer_task(self):
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
                    "and text()='FINALLY_PROJ']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'text-no-wrap') "
                    "and text()='ДОСКА ФИНАЛЬНАЯ']",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'text-no-wrap') "
                    "and text()='SkripnikovaFINAL']",
                )
            )
        ).click()
        sleep(2)

    def delete_task(self):
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

