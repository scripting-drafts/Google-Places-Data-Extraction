from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import csv
import itertools
import re
from tqdm import tqdm

concept = input('What are you looking for?:\n')

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
path = './' + str(startDate) + ' ' + start + ' ' + 'barcelona-' + concept + '.csv'
row = 0
col = 0
searchLevel = 1
locationList = []
locationSet = ()

data = {
    'name':[],
    'address':[],
    'rate':[],
    'comments':[],
    'type':[]
}

class mapsSearch:
    def setDriver(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.get('https://www.google.com/maps/')

        self.driver = driver

    def getDriver(self):
        return self.driver

    def zoomSearch(self):
        try:
            zoomIn = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-zoom-in')))
            self.driver.find_element_by_id('widget-zoom-in').click()
            time.sleep(3) #6
            searchThisArea = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'widget-search-this-area-inner')))
            self.driver.find_element_by_class_name('widget-search-this-area-inner').click()
            time.sleep(3) #6
        except TimeoutException:
            print('zoomSearch:TimeoutException')
            pass
        except ElementNotInteractableException:
            print('zoomSearch:ElementNotInteractableException | Skipping neighbourhood')
            pass

def unique_everseen(iterable, key=None):
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def write_csv(data, path, mode="w"):
    with open(path, mode) as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(data.keys())
        writer.writerows(zip(*data.values()))

ms = mapsSearch()
ms.setDriver()

####################################### GET PLACES
for barri in tqdm(barris):
    try:
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.COMMAND + 'a')
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(barri + ' barcelona' + Keys.RETURN)
    except ElementNotInteractableException:
        ms.getDriver().get('https://www.google.com/maps/')
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(barri + ' barcelona' + Keys.RETURN)
    time.sleep(6)
    try:
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.COMMAND + 'a')
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(concept + Keys.RETURN)
    except ElementNotInteractableException:
        time.sleep(4)
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.COMMAND + 'a')
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(concept + Keys.RETURN)
    time.sleep(4)
    ms.zoomSearch()
    searchLevel = 1
    while searchLevel <= 6:
        try:
            sectionResultsRAW = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.section-result-title')))
            sectionResultsLocationRAW = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.section-result-location')))
        except TimeoutException:
            print('1 List empty: Skipping neighbourhood')
            break
        else:
            for (sectionResult, sectionResultLocation) in itertools.zip_longest(sectionResultsRAW, sectionResultsLocationRAW, fillvalue =''):
                locationList.append([sectionResult.text, sectionResultLocation.text])
        ms.zoomSearch()
        try:
            emptyList = ms.getDriver().find_element_by_css_selector('.section-no-result-title')
        except NoSuchElementException:
            pass
        else:
            print('2 List empty: Skipping neighbourhood')
            break
        searchLevel += 1

################################## FILTER DUPLICATES
locationSet = list(unique_everseen(locationList, key=frozenset))

################################## SEARCH PLACES
for (sectionResult, sectionResultLocation) in tqdm(locationSet):
    try:
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(Keys.COMMAND + 'a')
    except ElementNotInteractableException:
        ms.getDriver().get('https://www.google.com/maps/')
    finally:
        ms.getDriver().find_element_by_id('searchboxinput').send_keys(sectionResult + " " + sectionResultLocation + Keys.RETURN)
    time.sleep(4)
    try:
        newTitle = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-hero-header-title-title')))
        newLocation = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-info-text')))
        cleanNewTitle = newTitle.text
        cleanNewLocation = newLocation.text
    except TimeoutException:
        try:
            click = WebDriverWait(ms.getDriver(), 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.section-result-title')))
            ms.getDriver().find_element_by_css_selector('.section-result').click()
            time.sleep(4)
            try:
                newTitle = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-hero-header-title-title')))
                newLocation = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-info-text')))
                cleanNewTitle = newTitle.text
                cleanNewLocation = newLocation.text
            except TimeoutException:
                print('#TimeoutException: Something is wrong')
                pass
            else:
                try:
                    starsRate = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-star-display')))
                    cleanStarsRate = float((starsRate.text).replace(',','.'))
                except TimeoutException:
                    cleanStarsRate = ''
                    pass
                try:
                    commentsNum = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-rating-term-list > span:nth-child(1) > span:nth-child(2) > span:nth-child(1) > button:nth-child(1)')))
                    subCommentsNum = re.sub('[()]', '', str(commentsNum.text))
                    cleanCommentsNum = int(subCommentsNum.replace('.', ''))
                except TimeoutException:
                    cleanCommentsNum = ''
                    pass
                try:
                    placeType = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.GLOBAL__gm2-body-2:nth-child(2) > span:nth-child(1) > span:nth-child(1) > button:nth-child(1)')))
                    cleanPlaceType = placeType.text
                except TimeoutException:
                    cleanPlaceType = ''
                    pass
        except TimeoutException:
            print('2 TimeoutException in click')
            pass
        except ElementClickInterceptedException:
            print('2 ElementClickInterceptedException')
            pass
    else:
        try:
            starsRate = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-star-display')))
            cleanStarsRate = float((starsRate.text).replace(',','.'))
        except TimeoutException:
            cleanStarsRate = ''
            pass
        try:
            commentsNum = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.section-rating-term-list > span:nth-child(1) > span:nth-child(2) > span:nth-child(1) > button:nth-child(1)')))
            subCommentsNum = re.sub('[()]', '', str(commentsNum.text))
            cleanCommentsNum = int(subCommentsNum.replace('.', ''))
        except TimeoutException:
            cleanCommentsNum = ''
            pass
        try:
            placeType = WebDriverWait(ms.getDriver(), 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.GLOBAL__gm2-body-2:nth-child(2) > span:nth-child(1) > span:nth-child(1) > button:nth-child(1)')))
            cleanPlaceType = placeType.text
        except TimeoutException:
            cleanPlaceType = ''
            pass
    finally:
        data['name'].append(cleanNewTitle)
        data['address'].append(cleanNewLocation)
        data['rate'].append(cleanStarsRate)
        data['comments'].append(cleanCommentsNum)
        data['type'].append(cleanPlaceType)
ms.getDriver().quit()

print(data)

write_csv(data, path)

endDate = datetime.date.today()
end = time.strftime("%H:%M:%S")

print(concept.upper() + '\nTime elapsed:\n' + str(startDate) + ' ' + start + '\n' + str(endDate) + ' ' + end)
