from selenium import webdriver 
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import time, sleep
import traceback
from config import token
import peewee
from models import *
from tbot import *
import os
import datetime


bot = telebot.TeleBot(token)

def open_webdriver(url):
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized') 
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36') 
    chrome_options.add_argument('origin=https://loads.ati.su') 
    chrome_options.add_argument('referer=https://loads.ati.su') 
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options = chrome_options)
    driver = autorizaite(driver)
    driver.get(url)
    sleep(2)
    return driver


def autorizaite(driver):
    auth = 'https://id.ati.su/login/'
    username = ''
    password = ''
    driver.get(auth)
    wait = WebDriverWait(driver, 500)
    wait.until(EC.element_to_be_clickable((By.ID, "login")))

    log = driver.find_element_by_id('login').send_keys(username)
    pswd = driver.find_element_by_id('password').send_keys(password)
    sleep(0.2)
    enter = driver.find_element_by_id('action-login').send_keys(Keys.ENTER)
    sleep(3)
    return driver


id_list = []

def move_parsing(main_link, UID,driver = None):

    last = ''
    if driver == None:
        driver = open_webdriver(main_link)


    try:
        while True:
            if not Search.select().where(Search.URL == main_link):
                driver.quit()
                break

            table = driver.find_element_by_id('pretty-loads-holder')
            section = table.find_elements_by_xpath('.//div[@data-app="pretty-load"]')
            for one in section:
                data_load = one.get_attribute('data-load-id')
                id = one.find_elements_by_xpath('.//span')[0].text


                if one.find_elements_by_xpath('.//button[@type="button"]'):
                    button = one.find_element_by_xpath('.//button[@type="button"]').click()
                    sleep(1)

                tag = '_1sWLx'#driver.find_element_by_xpath('//*[@id="pretty-loads-holder"]/div[2]/div/div/div[8]/div[1]/div[3]/div/div[2]/div[1]/span/div/span/a').get_attribute('class')
                data = driver.find_element_by_xpath(f'//div[@data-load-id="{data_load}"]')

                if id not in id_list:
                    data.location_once_scrolled_into_view
                    driver.execute_script("window.scrollTo(0, -100)") 
                    sleep(0.1)

                    id_list.append(id)
                    phone = []
                    for oph in one.find_elements_by_xpath(f'.//a[@class="{tag}"]'):
                        phone.append(oph.text)
                    phone = '\n'.join(phone)


                    data.screenshot(f'ph/{id}.png')
                    sleep(1)
                    print(id, datetime.datetime.now())


                    photo = open(f'ph/{id}.png', 'rb')
                    bot.send_photo(UID, photo = photo, caption = phone )

                    if last != '':
                        os.remove(last)
                        last = f'ph/{id}.png'
                    else:
                        last = f'ph/{id}.png'

                    



            refresh = driver.find_element_by_id('weightFrom')
            refresh.location_once_scrolled_into_view
            sleep(0.1)
            refresh.send_keys(Keys.ENTER)
            sleep(1)

            




    except Exception as error:
        print(traceback.format_exc(), '\n\n', error)
        driver.get(main_link)
        sleep(5)
        return move_parsing(main_link, UID, driver)        



