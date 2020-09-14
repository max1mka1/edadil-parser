from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import os,time


path = os.getcwd()
chromedriver_path = os.path.join(path,"chrome_driver","chromedriver.exe")
service = Service(chromedriver_path)
service.start()
driver = webdriver.Remote(service.service_url)
driver.implicitly_wait(10)


def get_links(url,selector):
categories = driver.find_elements_by_class_name(selector)
list_links = []
for category in categories:
print(category.text)
#print(categories)
return categories



retailers_selector = "pdo-inline-block"
retailers_url = "https://mercadao.pt/store/pingo-doce"
driver.get(retailers_url)
time.sleep(3)
retailers_links = get_links(url=retailers_url, selector=retailers_selector)
print(retailers_links)
retailers_links[2]
ui = driver.find_element_by_class_name("pdo-store-sidebar")
print(ui)
select = Select(ui)
select.select_by_index(2)



driver.quit()