from time import sleep
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


load_dotenv()

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

driver = webdriver.Chrome(executable_path="C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapInstaFollowers\\chromedriver.exe")
driver.maximize_window()

insta_url = "https://www.instagram.com/"
driver.get(insta_url)

sleep(3)

username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
username_field.send_keys(USERNAME)

sleep(3)


password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
password_field.send_keys(PASSWORD)

sleep(3)

login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
login_button.click()

sleep(10)

login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
login_button.click()
