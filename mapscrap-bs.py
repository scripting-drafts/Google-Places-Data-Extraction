from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


urlMaps = "https://www.google.com/maps/"
concept = input("Quina es la tipologia del negoci?:")

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(urlMaps)

#level_content = BeautifulSoup(driver.page_source, "html.parser")

driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(concept)
driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(Keys.RETURN)

level_content = BeautifulSoup(driver.page_source, "html.parser")

for locationString in level_content.find_all('span', class_="section-result-location"):
    location = locationString.get_text()
    print(location)
driver.close()
