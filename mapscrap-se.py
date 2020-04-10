from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


urlMaps = "https://www.google.com/maps/"
concept = input("Quina es la tipologia del negoci?:")

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(urlMaps)

driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(concept)
driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(Keys.RETURN)

for locations in driver.find_elements_by_class_name('section-result-location'):
    location = locations.text
    print(location)

driver.close()
