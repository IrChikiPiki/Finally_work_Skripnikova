.PHONY: help test test-api test-ui test-all test-parallel clean

help:
	@echo "📋 Доступные команды:"
	@echo "  make test-api      - Запуск API тестов"
	@echo "  make test-ui       - Запуск UI тестов"
	@echo "  make test-all      - Запуск всех тестов"
	@echo "  make test-parallel - Параллельный запуск"
	@echo "  make test-smoke    - Дымовые тесты"
	@echo "  make allure        - Открыть Allure отчет"

test-api:
	pytest -m api -v --alluredir=allure-results

test-ui:
	pytest -m ui -v --alluredir=allure-results

test-all:
	pytest -v --alluredir=allure-results

test-parallel:
	pytest -n auto -v --alluredir=allure-results

test-smoke:
	pytest -m smoke -v

allure:
	allure serve allure-results

clean:
	rm -rf allure-results/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +