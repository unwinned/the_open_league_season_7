from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pywinauto import Application
import time
import datetime
import os
import pyautogui as pag
import sys

# кол-во TON для свапа на NOT
amount_of_crypto = int(input("Введи количество TON для свапов (числа с точками недопустимы): "))

# кол-во успешных транз (если здесь будет 3, то всего 3 транзы будет, 5=5 и тд.)
amount_of_cycles = int(input("Введи количество циклов (2 транзакции за раз): "))

# спасибо
thanks = input("Записал. Спасибо. Приятного использования :) \n (p.s: для продолжения жми enter)")

print("Made by unwinned | тгк: unwinnedcrypto")

# сделано транзакций
made_cycles = 0


tonkeeper_window = Application(backend="uia").connect(title_re="Tonkeeper Pro")
rulekeeper = tonkeeper_window.window(title_re="Tonkeeper Pro")
confirm_button = rulekeeper.child_window(title="Confirm", control_type="Button")
connect_button = rulekeeper.window(title="Connect wallet", control_type="Button")

url = f"https://swap.coffee/dex?ft=TON&st=EQAvlWFDxGF2lXm67y4yzC17wYKD9A0guwPkMs1gOsM__NOT&fa={amount_of_crypto}"

# запуск webdriver без графического интерфейса для вычисления спрэда
options = Options()

# для того чтобы не было лишних принтов в консоль
options.add_argument("--log-level=3")
os.environ["WDM_LOG_LEVEL"] = "0"

# поиск webdriver в текущей папке
base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
driver_path = os.path.join(base_path, "chromedriver.exe")
driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)

MAX_RETRIES = 100000

driver.get(url)

app = Application(backend="uia").connect(title_re=".*Google Chrome.*")
chrome_window = app.window(title_re=".*Google Chrome.*")
coffee_swap_tab = chrome_window.child_window(title_re=".*swap.coffee*", control_type="TabItem") 
chrome_window.set_focus()

# время на настройку
time.sleep(30)

def swap():
    retries = 0
    chrome_window.set_focus()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/label/input'))).click()
    pag.press(["backspace"], 10)
    pag.write(str(amount_of_crypto))
    time.sleep(3)

    try:
       WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div[2]/div/div[2]/div[2]/div[1]/div[5]/button'))).click()
    except:
            while retries < MAX_RETRIES:
                try:
                    print("Пробую еще раз...")
                    pag.press(["F5"])
                    time.sleep(4)
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/label/input'))).click()
                    pag.press(["backspace"], 10)
                    pag.write(str(amount_of_crypto))
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div[2]/div/div[2]/div[2]/div[1]/div[5]/button'))).click()
                    break
                except:
                    print(f"Attempt {retries + 1}")
                    if retries < MAX_RETRIES:
                        print("Пробую еще раз...")
                        pag.press("F5")  # Refresh the page
                        time.sleep(4)
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/label/input'))).click()
                            pag.press("backspace", presses=10)
                            pag.write(str(amount_of_crypto))
                        except:
                            print("Неудалось крч")
                    else:
                        print("Достигнуто максимальное количество попыток")
    time.sleep(8)
    rulekeeper.set_focus()
    time.sleep(5)
    confirm_button.click_input()
    time.sleep(3)
    chrome_window.set_focus()
    time.sleep(7)
    pag.hotkey("ctrl", "w")
    time.sleep(90)

    # закрываем утку нахуй
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "success__close-btn"))).click()

    time.sleep(5)

    pag.press(["F5"])
    time.sleep(7)
    pag.press(["F5"])
    time.sleep(7)

    # поменять токены местами
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/button'))).click()

    time.sleep(7)

    # max
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/button'))).click()
    
    time.sleep(5)

    # swap
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//div/div[2]/div/div[2]/div[2]/div[1]/div[5]/button'))).click()
    time.sleep(4)

    rulekeeper.set_focus()
    time.sleep(8)
    confirm_button.click_input()
    time.sleep(5)

    chrome_window.set_focus()
    time.sleep(3)
    pag.hotkey("ctrl", "1")
    time.sleep(90)

    # закрываем утку нахуй
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "success__close-btn"))).click()

    time.sleep(3)

    # поменять токены местами
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/button'))).click()

while made_cycles < amount_of_cycles:
    swap()
    with open('done.txt', 'a') as file:
        file.write(f"Цикл был сделан {datetime.datetime.now()}" + '\n')
    print("Цикл сделан и записан")
    made_cycles += 1
