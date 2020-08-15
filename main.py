from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
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

    data = {'description': [], 'categories': [], 'retailer': [],
            'quantity': [], 'dates': [], 'new_price': [],
            'old_price': [], 'discount': [],  'image': [], 'link': []}

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

    def page_has_loaded(self):
        # print(f"Checking if {self.browser.current_url} page is loaded")
        page_state = self.browser.execute_script('return document.readyState;')
        return page_state == 'complete'

    def parse_page(self, url):
        '''
        Метод parse_page() парсит страницу с конкретным товаром
        :param url: Ссылка на товар
        :return: Объект Dict - словарь с информацией по товару
        '''
        dict_of_info = {}
        try:
            # Переход на страницу входа
            self.browser.get(url)
            page_is_ready = self.page_has_loaded()
            while page_is_ready != True:
                page_is_ready = self.page_has_loaded()
                sleep(0.3)
                print(f'0.3')
            try:
                retailer = self.browser.find_element_by_class_name("p-offer__retailer-title")
                retailer = retailer.text
            except NoSuchElementException:
                retailer = '-'
                logging.exception(f'NoSuchElementException: retailer')
                pass
            try:
                dates = self.browser.find_element_by_class_name("p-offer__dates")
                dates = dates.text
            except NoSuchElementException:
                dates = '-'
                logging.exception(f'NoSuchElementException: dates')
                pass
            try:
                image = self.browser.find_element_by_class_name("b-image__img")
                image = image.get_attribute("src")
            except NoSuchElementException:
                image = '-'
                logging.exception(f'NoSuchElementException: image')
                pass
            try:
                description = self.browser.find_element_by_class_name("p-offer__description")
                description = description.text
            except NoSuchElementException:
                description = '-'
                logging.exception(f'NoSuchElementException: description')
                pass
            try:
                new_price = self.browser.find_element_by_class_name("p-offer__price-new")
                new_price = new_price.text
                new_price = new_price.replace(',', '.')
                new_price = new_price.split()[0]
            except NoSuchElementException:
                new_price = '-'
                logging.exception(f'NoSuchElementException: new_price')
                pass
            old_price = self.browser.find_elements_by_class_name("p-offer__price-old")
            if len(old_price) == 0:
                old_price = '-'
            else:
                old_price = self.browser.find_element_by_class_name("p-offer__price-old")
                old_price = old_price.text
                old_price = old_price.replace(',', '.')
                old_price = old_price.split()[0]
                # print(f"old_price = {old_price}")
            discount = self.browser.find_elements_by_class_name("p-offer__discount")
            if len(discount) == 0:
                discount = '-'
            else:
                discount = self.browser.find_element_by_class_name("p-offer__discount")
                discount = discount.text
            all_categories = self.browser.find_elements_by_class_name("p-offer__segment-path")
            if len(all_categories) == 0:
                categories = '-'
            else:
                categories = []
                for category in all_categories:
                    categories.append(category.text)
                categories = ','.join(categories)
            try:
                quantity = self.browser.find_element_by_class_name("p-offer__quantity")
                quantity = quantity.text
                # print(f"quantity = {quantity}")
            except:
                quantity = '-'
                pass

            # Можно также парсить похожие категории товаров
            # similar = self.browser.find_element_by_class_name("p-offer__similar-offers")
            dict_of_info = {'description': description, 'categories': categories, 'retailer': retailer,
                            'quantity': quantity, 'dates': dates, 'new_price': new_price, 'old_price': old_price,
                            'discount': discount, 'image': image, 'link': url}
            return dict_of_info
        except Exception as e:
            print(e)
            logging.info(f'Exception {e}')
        finally:
            return dict_of_info


    def get_all_links_on_page(self, url):
        sleep(0.3)
        links = []
        elems = self.browser.find_elements_by_xpath("//a[@href]")  # p-index__retailer
        for elem in elems:
            link = elem.get_attribute("href")
            # print(f'link = {link}')
            links.append(link)
        return links


    def parse_url_for_classname(self, url, class_name):
        # This function gets all links from url according to class_name
        links = []
        try:
            self.browser.get(url)
            sleep(3)
            elems = self.browser.find_elements_by_class_name(class_name)
            links = [elem.get_attribute('href') for elem in elems]
        except Exception as e:
            print(e)
            logging.info(f'Exception {e}')
        finally:
            return links


    def print_dict(self, dict_of_info):
        for key, value in dict_of_info.items():
            print(f'{key}: {value}')


    def save_list_to_txt(self, list_to_save, name):
        file_path = os.path.join(os.getcwd(), "info_files")
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(file_path, name + ".txt")
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, mode="w") as f:
            for string in list_to_save:
                f.write(string + '\n')
        print(f"File {name + '.txt'} sucsessfully saved!")


    def create_databases(self, database, all_dict_of_info):
        path = os.path.join(os.getcwd(), 'info_files')
        database.to_excel(os.path.join(path, "Edadil_database.xlsx"), sheet_name='Sheet_name_1')
        print(f"Database .xlsx created sucsessfully!")
        database.to_csv(os.path.join(path, 'Edadil_database.csv'), sep=',')
        print(f"Database .csv created sucsessfully!")
        '''
        with open("Edadil_database.txt", "w") as text_file:
            for dict_ in all_dict_of_info:
                for key, val in dict_.items():
                    text_file.write(val)
                    text_file.write(';')
                text_file.write('\n')
        print(f"Database .txt created sucsessfully!")
        '''

def main():

    parser = EdadilParser()
    retailers_url = 'https://edadeal.ru/chelyabinsk/retailers'
    retailer_classname = "p-retailers__retailer" # "p-retailers__retailer p-retailers__retailer_empty_false"
    retailers_links = parser.parse_url_for_classname(url=retailers_url, class_name=retailer_classname)
    #retailers_links = parser.parse_url_for_classname(url=retailers_url, class_name="p-index__retailer")
    parser.save_list_to_txt(retailers_links, "retailers_links")
    buttons_classname = "b-button__root"
    goods_offers = "p-retailer__offer"
    print(f'Количество магазинов = {len(retailers_links)}')

    all_goods_links, all_pages_links = [], []
    for retailer_link in tqdm(retailers_links[8:9]):
        pages_links = parser.parse_url_for_classname(url=retailer_link, class_name=buttons_classname)
        pages_links = [link for link in pages_links if ((type(link) is not type(None)) and ('page=' in link))]
        all_pages_links.append(retailer_link)
        for page_link in pages_links:
            all_pages_links.append(page_link)
    print(f'Количество ссылок на все страницы магазинов = {len(all_pages_links)}')
    parser.save_list_to_txt(all_pages_links, "all_pages_links")

    for page_link in tqdm(all_pages_links):
        goods_links_from_page_links = parser.parse_url_for_classname(url=page_link, class_name=goods_offers)
        for good_link in goods_links_from_page_links:
            all_goods_links.append(good_link)

    database = pd.DataFrame(data=parser.data)
    all_goods_links = [link for link in all_goods_links if (type(link) is not type(None))]
    print(f'Количество ссылок на товары = {len(all_goods_links)}')
    parser.save_list_to_txt(all_goods_links, "all_goods_links")

    all_dict_of_info = []
    counter = Count()
    for good_link in tqdm(all_goods_links[:2]):
        dict_of_info = parser.parse_page(url=good_link)
        all_dict_of_info.append(dict_of_info)
        i = next(counter)
        print(f"{i} - {dict_of_info}")
        if type(dict_of_info) == dict:
            for key, val in dict_of_info.items():
                database.loc[i, key] = val

    #database.to_excel("Edadil_database.xlsx", sheet_name='Sheet_name_1')
    #print(f"Database .xlsx created sucsessfully!")
    #database.to_csv('Edadil_database.csv', sep=',')
    #print(f"Database .csv created sucsessfully!")
    parser.create_databases(database, all_dict_of_info)
    sleep(0.3)
    parser.browser.close()
    parser.browser.quit()


if __name__ == '__main__':
    main()