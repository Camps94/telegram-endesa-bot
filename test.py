#!/usr/local/opt/python/libexec/bin/python

from selenium import webdriver
import time
import psycopg2


driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
link = 'http://med-menuonline.com/endesaOcupacion.php?max=850&orientacion=horizontal'
driver.get(link)
occupancy = driver.find_element_by_tag_name('text.ct-label').text
print('\n' , occupancy)

driver.close() 