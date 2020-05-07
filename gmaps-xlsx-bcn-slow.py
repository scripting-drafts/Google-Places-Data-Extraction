from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import subprocess
import xlsxwriter
import itertools

concept = input('Quina classe d\'establiment estàs buscant?:\n')

barris = ['Barceloneta','Barri Gòtic', 'El Raval', 'Sant Pere', 'Santa Caterina', 'La Ribera',
'Antiga Esquerra de l\'Eixample', 'Nova Esquerra de l\'Eixample', 'Dreta de l\'Eixample',
'Fort Pienc', 'Sagrada Família', 'Sant Antoni', 'La Bordeta', 'La Font de la Guatlla',
'Hostafrancs', 'La Marina de Port', 'La Marina de Prat Vermell', 'El Poblesec', 'Sants',
'Sants-Badal', 'Montjuïc', 'Zona Franca', 'Port', 'Les Corts', 'La Maternitat i Sant Ramon',
'Pedralbes', 'El Putget i Farró', 'Sarrià', 'Sant Gervasi - La Bonanova', 'Sant Gervasi - Galvany',
'Les Tres Torres', 'Vallvidrera', 'Tibidabo', 'Les Planes', 'Vila de Gràcia', 'Camp d\'en Grassot i Gràcia Nova',
'La Salut', 'Barri del Coll', 'Vallcarca i els Penitents', 'El baix Guinardó', 'El Guinardó',
'Can Baró', 'El Carmel', 'La Font d\'en Fargues', 'Horta', 'La Clota', 'Montbau', 'Sant Genís dels Agudells',
'La Teixonera', 'La Vall d\'Hebron', 'Can Peguera', 'Canyelles', 'Ciutat Meridiana', 'La Guineueta',
'Porta', 'Prosperitat', 'Les Roquetes', 'Torre Baró', 'Trinitat Nova', 'El Turó de la Peira',
'Vallbona', 'Verdum', 'Vilapicina', 'La Torre Llobeta', 'Baró de Viver', 'Bon Pastor', 'El Congrés i els Indians',
'Navas', 'Sant Andreu de Palomar', 'La Sagrera', 'Trinitat Vella', 'El Besòs i el Maresme', 'El Clot',
'El Camp de l\'Arpa del Clot', 'Diagonal Mar i el Front Marítim del Poblenou', 'El Parc i la llacuna del Poblenou',
'El Poblenou', 'Provençals del Poblenou', 'Sant Martí de Provençals', 'La Verneda', 'La Pau', 'Vila Olímpica del Poblenou']

startDate = datetime.date.today()
start = time.strftime("%H:%M:%S")
workbook = xlsxwriter.Workbook(str(startDate) + ' ' + 'barcelona-' + concept + '.xlsx')
worksheet = workbook.add_worksheet()
row = 1
searchPercent = 0
searchLevel = 1

class mapsSearch:
    def __init__(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.get('https://www.google.com/maps/')

        resultsDriver = webdriver.Firefox()
        resultsDriver.implicitly_wait(10)
        resultsDriver.get('https://www.google.com/maps/')

        self.driver = driver
        self.resultsDriver = resultsDriver

    def getDriver(self):
        return self.driver

    def getResultsDriver(self):
        return self.resultsDriver

    def zoomSearch(self):
        try:
            zoomIn = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-zoom-in')))
            self.driver.find_element_by_id('widget-zoom-in').click()
            time.sleep(4) #6
            searchThisArea = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-search-this-area-inner')))
            self.driver.find_element_by_class_name('widget-search-this-area-inner').click()
            time.sleep(4) #6
        except TimeoutException:
            print('zoomSearch:TimeoutException')
            pass
        except ElementNotInteractableException:
            print('zoomSearch:ElementNotInteractableException | Skipping neighbourhood')
            global searchLevel
            searchLevel = 7
            pass

ms = mapsSearch()

for barri in barris:
    ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.CONTROL + 'a')
    ms.getDriver().find_element_by_id('searchboxinput').send_keys(barri + ' barcelona' + Keys.RETURN)
    time.sleep(4)
    ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.CONTROL + 'a')
    ms.getDriver().find_element_by_id('searchboxinput').send_keys(concept + Keys.RETURN)
    time.sleep(4)
    ms.zoomSearch()
    print('Buscant establiments a ' + str(barri))
    searchLevel = 1
    while searchLevel <= 6:
        sectionResultsRAW = ms.getDriver().find_elements_by_css_selector('.section-result-title')
        sectionResultsLocationRAW = ms.getDriver().find_elements_by_css_selector('.section-result-location')
        try:
            for (sectionResult, sectionResultLocation) in itertools.zip_longest(sectionResultsRAW, sectionResultsLocationRAW, fillvalue = barri):
                    worksheet.write('C' + str(row), barri)
                    ms.getResultsDriver().find_element_by_id('searchboxinput').send_keys(Keys.CONTROL + 'a')
                    ms.getResultsDriver().find_element_by_id('searchboxinput').send_keys(sectionResult.text + " " + sectionResultLocation.text + Keys.RETURN)
                    time.sleep(6)
                    try:
                        newTitle = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-hero-header-title-title')))
                        newTitle = ms.getResultsDriver().find_element_by_css_selector('.section-hero-header-title-title').text
                        newLocation = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-info-text')))
                        newLocation = ms.getResultsDriver().find_element_by_css_selector('.section-info-text').text
                        worksheet.write('A' + str(row), newTitle)
                        worksheet.write('B' + str(row), newLocation)
                    except TimeoutException:
                        try:
                            click = WebDriverWait(ms.getResultsDriver(), 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.section-result-title')))
                            ms.getResultsDriver().find_element_by_css_selector('.section-result').click()
                            time.sleep(6)
                            try:
                                newTitle = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-hero-header-title-title')))
                                newTitle = ms.getResultsDriver().find_element_by_css_selector('.section-hero-header-title-title').text
                                newLocation = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-info-text')))
                                newLocation = ms.getResultsDriver().find_element_by_css_selector('.section-info-text').text
                                worksheet.write('A' + str(row), newTitle)
                                worksheet.write('B' + str(row), newLocation)
                            except TimeoutException:
                                try:
                                    click = WebDriverWait(ms.getResultsDriver(), 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.section-result-title')))
                                    ms.getResultsDriver().find_element_by_css_selector('.section-result').click()
                                    time.sleep(6)
                                    try:
                                        newTitle = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-hero-header-title-title')))
                                        newTitle = ms.getResultsDriver().find_element_by_css_selector('.section-hero-header-title-title').text
                                        newLocation = WebDriverWait(ms.getResultsDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-info-text')))
                                        newLocation = ms.getResultsDriver().find_element_by_css_selector('.section-info-text').text
                                        worksheet.write('A' + str(row), newTitle)
                                        worksheet.write('B' + str(row), newLocation)
                                    except TimeoutException:
#                                        print('1 TimeoutException in section-info-text')
                                        pass
                                except TimeoutException:
#                                    print('1 TimeoutException in section-result')
                                    pass
                                except ElementClickInterceptedException:
#                                    print('1 ElementClickInterceptedException')
                                    pass
                        except TimeoutException:
#                            print('2 TimeoutException in section-result')
                            pass
                        except ElementClickInterceptedException:
#                            print('2 ElementClickInterceptedException')
                            pass
                    finally:
                        print(time.strftime("%H:%M:%S") + '  Search level ' + str(searchLevel) + ': ' + str(searchPercent) + "%" + ' | ' + sectionResult.text)
                        searchPercent += 5
                        row += 1
        except StaleElementReferenceException:
            print('StaleElementReferenceException...')
            pass

        searchLevel += 1
        searchPercent = 0

        ms.zoomSearch()

        try:
            emptyList = ms.getDriver().find_element_by_css_selector('.section-no-result-title')
        except NoSuchElementException:
            pass
        else:
            print('List empty: Skipping neighbourhood')
            break

workbook.close()

ms.getResultsDriver().quit()
ms.getDriver().quit()

endDate = datetime.date.today()
end = time.strftime("%H:%M:%S")

print(concept.upper() + '\nTime elapsed:\n' + str(startDate) + ' ' + start + '\n' + str(endDate) + ' ' + end)

#upload = subprocess.Popen(["python3", "/Users/flatline/Desktop/code/Scrapers/nou-comerciant/2-xlsx-to-mymaps.py", concept, location], stdout=subprocess.PIPE)
#output = upload.communicate()[0]
#print(output)
