from selenium import webdriver
import time
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
        self.retailers_url = 'https://edadeal.ru/chelyabinsk/retailers'
        self.retailer_classname = "p-retailers__retailer" # "p-retailers__retailer p-retailers__retailer_empty_false"
        self.buttons_classname = "b-button__root"
        self.goods_offers = "p-retailer__offer"
        self.url = None
        self.chromedriver_path = './chromedriver_win32/chromedriver.exe'
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument('--proxy-server=tg://socks?server=2a01:4f9:c010:7f53::1&port=1984&user=Maxinstellar&pass=YOURPASSWORD')
        # self.options.add_argument('headless')  # для открытия headless-браузера
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=self.options)
        self.browser.implicitly_wait(0.3)  # seconds

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
            sleep(1)
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
        sleep(1)
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
            sleep(1)
            elems = self.browser.find_elements_by_class_name(class_name)
            links = [elem.get_attribute('href') for elem in elems]
            return links
        except Exception as e:
            print(e)
            logging.info(f'Exception {e}')
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

    def get_buttons_links(self, url, class_name):
        try:
            self.browser.get(url)
            sleep(2)
            shops_links = self.browser.find_elements_by_class_name(class_name)
            list_links = [shop.get_attribute("href") for shop in shops_links]
            # Удаляем невалидные ссылки
            visible_links = [link for link in list_links if ((type(link) is not type(None)) and ('page=' in link))]
            # print(f"visible_links = {visible_links}")
            # Находим номер максимального номера страницы
            if visible_links:
                max_page_number = max([int(link.split('page=')[-1]) for link in visible_links if ('page=' in link)])
                list_links = [url] + [f'{url}?page={i}' for i in range(2, max_page_number + 1)]
            else:
                max_page_number = 1
                list_links = [url]
            print(f"Количество страниц в магазине {url.split('/')[-1]}: {max_page_number}")
            # Генерируем список ссылок на страницы с товарами + ссылка на ритейлера
            #for link in list_links:
            #    print(f"{link}")
            return list_links
        except Exception as e:
            print(e)
            return []

    def parse_link(self, good_link):
        start = time.time()
        dict_of_info = self.parse_page(url=good_link)
        # all_dict_of_info.append(dict_of_info)
        i = next(self.counter)
        print(f"{i}/{self.all_goods_links_count}: {dict_of_info}")
        if type(dict_of_info) == dict:
            for key, val in dict_of_info.items():
                self.database.loc[i, key] = val
        end = time.time() - start
        print(f"Время выполнения парсинга товара: {end}")
        return dict_of_info, end



def main():

    parser = EdadilParser()
    retailers_links = parser.parse_url_for_classname(url=parser.retailers_url, class_name=parser.retailer_classname)
    # retailers_links = parser.parse_url_for_classname(url=retailers_url, class_name="p-index__retailer")
    parser.save_list_to_txt(retailers_links, "retailers_links")
    print(f'Количество магазинов = {len(retailers_links)}')

    print(f"retailers_links = {retailers_links}")
    all_goods_links, all_pages_links = [], []
    counter = Count()
    next(counter)
    for retailer_link in retailers_links:
        print(f"{next(counter)}) ", end='')
        pages_links = parser.get_buttons_links(url=retailer_link, class_name=parser.buttons_classname)
        for page_link in pages_links:
            all_pages_links.append(page_link)
    all_pages_count = len(all_pages_links)
    print(f'Количество ссылок на все страницы всех магазинов = {all_pages_count}')
    parser.save_list_to_txt(all_pages_links, "all_pages_links")
    #counter2 = Count()
    #next(counter)
    for page_link in tqdm(all_pages_links):
        goods_links_from_page_links = parser.parse_url_for_classname(url=page_link, class_name=parser.goods_offers)
        # print(f"page_link = {page_link.split('/')[-1]}, {goods_links_from_page_links}")
        for good_link in goods_links_from_page_links:
            all_goods_links.append(good_link)

    parser.database = pd.DataFrame(data=parser.data)
    all_goods_links = [link for link in all_goods_links if (type(link) is not type(None))]
    parser.all_goods_links_count = len(all_goods_links)
    print(f'Количество ссылок на товары = {parser.all_goods_links_count}')
    parser.save_list_to_txt(all_goods_links, "all_goods_links")

    print('Извлекаем данные в список словарей и сохраняем полученные данные')

    parser.counter = Count()
    all_dict_of_info, times = [], []
    for good_link in all_goods_links:
        dict_of_info, end_time = parser.parse_link(good_link)
        all_dict_of_info.append(dict_of_info)
        times.append(end_time)

    print(all_dict_of_info)
    if all_dict_of_info:
        print(f"Среднее время парсинга одной страницы: {sum(times) / len(all_dict_of_info)}")
    #database.to_excel("Edadil_database.xlsx", sheet_name='Sheet_name_1')
    #print(f"Database .xlsx created sucsessfully!")
    #database.to_csv('Edadil_database.csv', sep=',')
    #print(f"Database .csv created sucsessfully!")
    parser.create_databases(parser.database, all_dict_of_info)

    sleep(0.3)
    parser.browser.close()
    parser.browser.quit()


if __name__ == '__main__':
    main()