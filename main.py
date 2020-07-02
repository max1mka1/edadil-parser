from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
import logging
import pandas as pd
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException

class Count:
    """Iterator that counts upward forever."""
    def __init__(self, start=0):
        self.num = start

    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        return num


class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.
      locator - used to find the element
      returns the WebElement once it has the particular css class
      """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


class EdadilParser():
    '''
    Класс EdadilParser()
    '''

    def __init__(self):
        '''
        Конструктор класса EdadilParser()
        '''
        self.url = None
        self.chromedriver_path = './chromedriver_win32/chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--proxy-server=tg://socks?server=2a01:4f8:c2c:5df::1&port=9388&user=maxinstellar&pass=english2011')
        #self.options.add_argument('headless')  # для открытия headless-браузера
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=self.options)
        self.browser.implicitly_wait(10)  # seconds

    def parse_page(self, url):
        '''
        Метод parse_page() парсит страничку с конкретным товаром
        :param self: Доступ к свойствам класса EdadilParser
        :param url: Ссылка на товар
        :return: Объект pandas.DataFrame - строка с информацией по товару
        '''
        sleep(1)
        dict_of_info = {}
        try:
            # Переход на страницу входа
            self.browser.get(url)
            #similar = WebDriverWait.until(element_has_css_class((By.ID, 'myNewInput'), "p-offer__similar-offers"))
            #view = WebDriverWait(self.browser, 10).until(
            #    EC.presence_of_element_located((By.ID, "view"))
            #)
            sleep(1)
            # Поиск тегов по имени классов
            #retailer, dates, image, new_price, old_price, description = '', '', '', '', '', ''
            retailer = self.browser.find_element_by_class_name("p-offer__retailer-title")
            dates = self.browser.find_element_by_class_name("p-offer__dates")
            image = self.browser.find_element_by_class_name("b-image__img")
            description = self.browser.find_element_by_class_name("p-offer__description")
            new_price = self.browser.find_element_by_class_name("p-offer__price-new")
            try:
                old_price = self.browser.find_element_by_class_name("p-offer__price-old")
                old_price = old_price.text
                old_price.encode("utf-8")
            except Exception as e:
                old_price = '-'
            old_price = '-'
            """
            try:
                retailer = self.browser.find_element_by_class_name("p-offer__retailer-title")
                retailer = retailer.text
                retailer.encode("utf-8")
            except NoSuchElementException:
                retailer = '-'.encode("utf-8")
                logging.exception(f'NoSuchElementException: retailer')
            try:
                dates = self.browser.find_element_by_class_name("p-offer__dates")
                dates = dates.text
                dates.encode("utf-8")
            except NoSuchElementException:
                dates = '-'.encode("utf-8")
                logging.exception(f'NoSuchElementException: dates')
            try:
                image = self.browser.find_element_by_class_name("b-image__img")
                image = image.get_attribute("src")
                image.encode("utf-8")
            except NoSuchElementException:
                image = '-'.encode("utf-8")
                logging.exception(f'NoSuchElementException: image')
            try:
                description = self.browser.find_element_by_class_name("p-offer__description")
                description = description.text
                description.encode("utf-8")
            except NoSuchElementException:
                description = '-'.encode("utf-8")
                logging.exception(f'NoSuchElementException: description')
            try: #
                new_price = self.browser.find_element_by_class_name("p-offer__price-new")
                new_price = new_price.text
                new_price.encode("utf-8")
            except NoSuchElementException:
                new_price = '-'.encode("utf-8")
                logging.exception(f'NoSuchElementException: new_price')
            try:
                old_price = self.browser.find_element_by_class_name("p-offer__price-old")
                old_price = old_price.text
                old_price.encode("utf-8")
            except NoSuchElementException:
                old_price = '-'.encode("utf-8")
            """
            # similar = self.browser.find_element_by_class_name("p-offer__similar-offers")
            #dict_of_info = {'retailer': retailer, 'dates': dates,
            #                'image': image, 'description': description,
            #                'new_price': new_price, 'old_price': old_price}
            dict_of_info = {'retailer': retailer.text, 'dates': dates.text,
                            'image': image.get_attribute("src"), 'description': description.text,
                            'new_price': new_price.text, 'old_price': old_price}
            # 'similar': similar.text}
            return dict_of_info
        except Exception as e:
            print(e)
        finally:
            return dict_of_info

    def get_all_links_on_page(self, url):
        sleep(0.3)
        links = []
        elems = self.browser.find_elements_by_xpath("//a[@href]")  # p-index__retailer
        for elem in elems:
            link = elem.get_attribute("href")
            print(f'link = {link}')
            links.append(link)
        return links

    def parse_url_for_classname(self, url, class_name):
        # This function gets all links from url according to class_name
        sleep(1)
        links = []
        try:
            self.browser.get(url)
            sleep(5)
            elems = self.browser.find_elements_by_class_name(class_name)
            links = [elem.get_attribute('href') for elem in elems]
        except Exception as e:
            logging.info(f'Exception {e}')
        finally:
            return links


    def print_dict(self, dict_of_info):
        for key, value in dict_of_info.items():
            print(f'{key}: {value}')

def main():
    parser = EdadilParser()
    retailers_url = 'https://edadeal.ru/chelyabinsk'
    retailers_links = parser.parse_url_for_classname(url=retailers_url, class_name="p-index__retailer")
    buttons_classname = "b-button__root"
    goods_offers = "p-retailer__offer"
    print(f'retailers_links = {retailers_links}')
    all_goods_links = []
    all_pages_links = []
    print(f'len = {len(retailers_links)}')
    for retailer_link in retailers_links:
        pages_links = parser.parse_url_for_classname(url=retailer_link, class_name=buttons_classname)
        print(f'len = {len(pages_links)}, {pages_links}')
        pages_links = [link for link in pages_links if ((type(link) is not type(None)) and ('page=' in link))]
        print(f'len = {len(pages_links)}, {pages_links}')
        all_pages_links.append(retailer_link)
        for page_link in pages_links:
            all_pages_links.append(page_link)
    print(f'len all_pages_links = {len(all_pages_links)}, all_pages_links = {all_pages_links}')
    '''
    for page_link in all_pages_links:
        goods_links_from_page_links = parser.parse_url_for_classname(url=page_link, class_name=goods_offers)
        print(f'goods_links_from_page_links = {goods_links_from_page_links}')
        for good_link in goods_links_from_page_links:
            all_goods_links.append(good_link)
    data = {'retailer': [], 'dates': [], 'image': [],
            'description': [], 'new_price': [], 'old_price': []}
    counter = Count()
    database = pd.DataFrame(data=data)
    print(f'len = {len(all_goods_links)}, all_goods_links = {all_goods_links}')
    all_goods_links = [link for link in all_goods_links if (type(link) is not type(None))]
    print(f'len = {len(all_goods_links)}, all_goods_links = {all_goods_links}')

    all_dict_of_info = []
    for good_link in tqdm(all_goods_links):
        dict_of_info = parser.parse_page(url=good_link)
        parser.print_dict(dict_of_info)
        all_dict_of_info.append(dict_of_info)
        i = next(counter)
        for key, val in dict_of_info.items():
            print(type(val))
            database.loc[i, key] = val
    def create_txt():
        text_file = open("Output.txt", "w")
        for dict_ in all_dict_of_info:
            for key, val in dict_.items():
                text_file.write(key)
                text_file.write(',')
                text_file.write(val)
                text_file.write(';')
        text_file.close()
    database.to_excel("output.xlsx", sheet_name='Sheet_name_1')
    #print(database.head())
    #database.to_csv('Edadil_database.csv', sep=',')#, encoding='utf-8')# , sep=',', encoding='cp1251')
    #link = "https://edadeal.ru/chelyabinsk/offers/e4dccd20-5a71-475a-83bc-ecf3170f8e0d?from=%2Fchelyabinsk%2Fretailers%2Fkrasnoeibeloe"
    #dict_of_info = parser.parse_page(url=link)
    #parser.print_dict(dict_of_info)
    '''
    sleep(0.3)
    parser.browser.close()
    parser.browser.quit()


if __name__ == '__main__':
    main()


'''
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from urllib.request import urlopen
'''
# a = browser.find_element_by_css_selector("p-offer__quantity")# price-new
#email = browser.find_element_by_name('ctl00$MainContent$ctlLogin$view')
#password = browser.find_element_by_name('ctl00$MainContent$ctlLogin$_Password')
#login = browser.find_element_by_name('ctl00$MainContent$ctlLogin$BtnSubmit')
# добавление учётных данных для входа
#email.send_keys('********')
#password.send_keys('*******')
# нажатие на кнопку отправки
#login.click()
# print(email)