from .pages.YouGile_pages import LoginYouGilePage, MainYouGilePage


def test_YouGile(driver_Chrome):
    """Тестирование YouGile"""

    # Производим Login
    login_page = LoginYouGilePage(driver_Chrome)
    login_page.login()

    # Создаём задачу
    main_page = MainYouGilePage(driver_Chrome)
    main_page.create_task()

    # Получаем название созданной задачи
    task_name = main_page.get_task_name()
    assert task_name == "Тестовая задача"

    # Назначаем исполнителя
    main_page.assign_performer()

    # Получаем имя назначенного исполнителя
    performer_name = main_page.get_performer_name()
    assert performer_name == "Ир"

    # Переносим задачу
    main_page.transfer_task()

    # Удаляем задачу
    main_page.delete_task()
