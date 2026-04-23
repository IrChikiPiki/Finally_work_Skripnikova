# YouGile Automation Tests

Автотесты для платформы YouGile.

**По проекту (финальная работа):** [Финальные проект по ручному тестированию "ru.yougile.com" .Скрипникова И. Н.](https://skripnikovainqa1182skypro.yonote.ru/share/312ecae6-207c-49fa-96e1-db31452ae54f)

## 🚀 Быстрый старт
(Для работы нужно создать и заполнить файл .env по образцу)

## Установка
```bash
git clone <repo-url>
cd yougile-tests
pip install -r requirements.txt
```

## Запуск тестов
### UI тесты (браузер)
pytest -m "ui" -v

### API тесты
pytest -m "api" -v

### Все тесты
pytest -v

### Headless режим для UI
pytest -m "ui" --headless -v

### Другой браузер (chrome/firefox)
pytest -m "ui" --browser=firefox -v

### Allure отчёт
pytest --alluredir=allure-results
allure serve allure-results

# Требования и Конфигурация

## 📋 Системные требования

### Минимальные требования
| Компонент | Версия     |
|-----------|------------|
| Python | 3.9+       |
| Chrome | 110+       |
| ОС | Windows 10 |
| RAM | 4 ГБ       |
| Дисковое пространство | 1 ГБ       |

### Зависимости Python
```txt
selenium>=4.15.0
pytest>=7.4.0
pytest-selenium>=4.0.0
requests>=2.31.0
allure-pytest>=2.13.0
webdriver-manager>=4.0.0
python-dotenv>=1.0.0
```

# Контакты

## 👨‍💻 Разработчик

**Имя:** Ирина Скрипников

**Email:** isokolova360@gmail.com

**GitHub:** [github.com/IrChikiPiki](https://github.com/IrChikiPiki)

---