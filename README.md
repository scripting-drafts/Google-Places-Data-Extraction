# Google-Data-Science

This is meant to be run on GNU/Linux but can be adapted to OSX by changing CONTROL keys to COMMAND keys.

Requirements:
 - Firefox
 - Geckodriver
 - Python3.7
 
 Libraries:
  - Selenium
  - tqdm
  - CSV
  - Itertools
  - Folium
  - Pandas
  - Branca
  
 - places-to-csv.py
 Scraps Google Maps by keyword given and writes it to a CSV file with UTF-8 encoding and semicolon delimiter.
 
 - csv-to-html-map.py
 Takes CSV file as argument. Creates a map with markers of all places classifying their Number of Comments by color and their Stars Rate by diameter of the marker.
