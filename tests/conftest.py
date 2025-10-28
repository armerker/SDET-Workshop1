import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure
import time

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    
    # астройка опций Chrome
    chrome_options = webdriver.ChromeOptions()
    
    # азовые настройки для стабильности
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        print("Установка ChromeDriver...")
        
        # спользуем webdriver-manager для автоматической загрузки драйвера
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("ChromeDriver успешно запущен")
        
    except Exception as e:
        print(f"шибка при запуске ChromeDriver: {e}")
        raise
    
    # Устанавливаем неявные ожидания
    driver.implicitly_wait(10)
    
    # ереход на целевую страницу
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager")
    
    # аем время для загрузки
    time.sleep(2)
    
    yield driver
    
    # акрытие браузера после теста
    driver.quit()
    print("раузер закрыт")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"е удалось сделать скриншот: {e}")
