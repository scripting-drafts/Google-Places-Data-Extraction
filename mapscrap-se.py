from selenium import webdriver
from selenium.webdriver.common.keys import Keys


urlMaps = "https://www.google.com/maps/"
concept = input("Quina es la tipologia del negoci?:")

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(urlMaps)

driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(concept + Keys.RETURN)

locations = driver.find_elements_by_class_name('section-result-location')

for location in locations:
    print(location.text)

driver.close()
