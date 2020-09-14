#pip install requests for installation

import requests

url = "https://backoffice.algoritmika.org/level-preview/32632?"
r = requests.get(url)
r.text

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os,time
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC

path = os.getcwd()
# chromedriver_path = os.path.join(path,"chrome_driver","chromedriver.exe")
chromedriver_path = './chromedriver_win32/chromedriver.exe'
service = Service(chromedriver_path)
service.start()
driver = webdriver.Remote(service.service_url)



class element_has_css_class(object):

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False



def get_links(url,selector):
    driver.get(url)
    time.sleep(3) # Let the user actually see something!
    shops_links = driver.find_elements_by_class_name(selector)
    list_links = []
    for shop in shops_links:
        link = shop.get_attribute("href")
        list_links.append(link)
    return list_links


page_num = "b-button__root"
retailers_selector = "p-retailers__retailer"
retailers_url = 'https://edadeal.ru/moskva/retailers'
retailers_links = get_links(url=retailers_url, selector=retailers_selector)
print(retailers_links)
magazine1 = get_links(url=retailers_links[0], selector=page_num)
print(magazine1)

from joblib import Parallel, delayed
# results = Parallel(n_jobs=-1, verbose=0, backend="threading")(map(delayed(parse_link), all_goods_links[:5]))
# for result in results:
#     print(f"!{result}")
# all_dict_of_info, times = Parallel(n_jobs=-1)(delayed(parse_link(good_link)) for good_link in tqdm(all_goods_links[:5]))


driver.quit()
"""