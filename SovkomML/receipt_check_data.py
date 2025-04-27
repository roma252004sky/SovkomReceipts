import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import logging

from ReceiptDTO import ReceiptDTO

# Настройка логгера
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Константы
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')  # Папка для загрузок
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Создаем папку, если не существует

def get_latest_downloaded_file(wait_time=30):
    """Получает последний скачанный файл из директории"""
    end_time = time.time() + wait_time
    while True:
        files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)]
        files = [f for f in files if os.path.isfile(f) and not f.endswith('.crdownload')]
        if files:
            return max(files, key=os.path.getctime)
        if time.time() > end_time:
            raise TimeoutError("Файл не был скачан за отведенное время")


def debug_info(driver):
    """Сбор отладочной информации"""
    try:
        logger.debug("Текущий URL: %s", driver.current_url)
        logger.debug("Высота страницы: %s", driver.execute_script("return document.body.scrollHeight"))
    except Exception as e:
        logger.error("Ошибка при сборе отладочной информации: %s", str(e))


def get_receipt_info(qr_data):
    options = webdriver.ChromeOptions()

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)

    actions = ActionChains(driver)

    try:
        logger.info("1. Открытие главной страницы")
        driver.get("https://proverkacheka.com/")
        debug_info(driver)

        logger.info("2. Поиск родительского контейнера")
        parent_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "b-checkform_tab-qrraw"))
        )
        logger.debug("Родительский элемент найден")

        logger.info("3. Поиск и активация кнопки 'Строка'")
        string_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Строка')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", string_button)
        driver.execute_script("arguments[0].click();", string_button)
        logger.info("Перешли в раздел 'Строка'")
        time.sleep(1)

        logger.info("4. Ввод данных")
        textarea = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea.b-checkform_qrraw"))
        )
        textarea.clear()
        textarea.send_keys(qr_data)

        # Снятие фокуса с поля ввода
        driver.find_element(By.TAG_NAME, 'body').click()
        debug_info(driver)

        logger.info("5. Поиск кнопки 'Проверить'")
        submit_button = WebDriverWait(parent_element, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.b-checkform_btn-send.btn-primary"))
        )

        # Проверка состояния кнопки
        WebDriverWait(driver, 5).until(
            lambda d: submit_button.is_displayed() and submit_button.is_enabled()
        )

        logger.info("6. Подготовка к клику")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", submit_button)
        actions.move_to_element(submit_button).pause(0.1).perform()

        # Комбинированная стратегия клика
        try:
            logger.info("Попытка 1: Клик через ActionChains")
            actions.click(submit_button).perform()
        except:
            logger.info("Попытка 2: Клик через JavaScript")
            driver.execute_script("arguments[0].click();", submit_button)

        logger.info("7. Ожидание результатов и скачивание файла")
        download_button = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button.btn.btn-primary.btn-sm.dropdown-toggle")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", download_button)
        actions.move_to_element(download_button).pause(0.01).perform()
        driver.execute_script("arguments[0].click();", download_button)

        # Клик на кнопку скачивания JSON
        download_button_second = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.b-check_btn-json"))
        )
        driver.execute_script("arguments[0].click();", download_button_second)

        # Ожидание завершения загрузки файла
        downloaded_file = get_latest_downloaded_file()
        logger.info(f"Скачан файл: {downloaded_file}")

        # Чтение и парсинг JSON
        with open(downloaded_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Удаление временного файла
        os.remove(downloaded_file)

        return data

    except Exception as e:
        logger.error("Ошибка: %s", str(e), exc_info=True)
        debug_info(driver)
        return None
    finally:
        driver.quit()


# Пример использования
# qr_data = "t=20221227T2025&s=262.84&fn=9960440502956695&i=34465&fp=1782149244&n=1"
# result = get_receipt_info(qr_data)
# print(ReceiptDTO(result).to_json())
# product_names = [item["name"] for item in result["items"]]
# print(product_names)



# rb = RuleBased()
# parsed_data = [rb.parse(name) for name in product_names]
# for i, result in enumerate(parsed_data, 1):
#     print(f"Товар {i}: {result}")
#print(json.dumps(result, indent=2, ensure_ascii=False))