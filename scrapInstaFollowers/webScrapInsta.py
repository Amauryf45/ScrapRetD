#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Insta_Info_Scraper:

    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def login_to_instagram(self, username, password):
        driver = webdriver.Chrome(executable_path="C:\\Users\\amaur\\Desktop\\Cours EMA\\2IA\\RetD\\scrapInstaFollowers\\chromedriver.exe")
        driver.maximize_window()

        insta_url = "https://www.instagram.com/"
        driver.get(insta_url)
        
        time.sleep(3)

        coockies_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]')))
        coockies_button.click()

        # Wait for the login page to load
        # Enter username and password
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(username)
        
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password_field.send_keys(password)

        # Click on the login button
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
        login_button.click()

        # Wait for the login process to complete
        time.sleep(5)

        # Return the driver after successful login
        return driver

    def getinfo(self, driver, url):
        driver.get(url)
        time.sleep(3)  # Wait for the page to load completely

        # Get the HTML content of the page
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'})
        text = data[0].get('content').split()
        user = '%s %s %s' % (text[-3], text[-2], text[-1])
        followers = text[0]
        following = text[2]
        posts = text[4]
        print('User:', user)
        print('Followers:', followers)
        print('Following:', following)
        print('Posts:', posts)
        print('—————————')

    def get_span_contents(self, driver, url):
        driver.get(url)
        time.sleep(3)  # Wait for the page to load completely

        # Get the HTML content of the page
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        spans = soup.find_all('span', class_='_ap3a _aaco _aacw _aacx _aad7 _aade')
        for span in spans:
            print(span.text)

    def main(self):
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']

        # Login to Instagram
        driver = self.login_to_instagram(username, password)

        with open('users.txt') as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            for url in content:
                self.getinfo(driver, url)
                time.sleep(2)
                url_followers = url + 'followers/'
                self.get_span_contents(driver, url_followers)
                #  temps to see
                time.sleep(10)
                login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
                login_button.click()

        # After scraping, close the browser
        driver.quit()

if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()
