#!/usr/local/opt/python/libexec/bin/python

from selenium import webdriver
import time
from datetime import datetime, timedelta
import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import os
import sys

CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', 'chromedriver')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')
options = Options()
options.binary_location = GOOGLE_CHROME_BIN
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.headless = True


email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
#driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
link = 'https://mediterranea.online/client/courses'
driver.get(link)
driver.find_element_by_id('email').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/div[3]/button").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/ul/li[4]/button").click()
time.sleep(15)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/button[3]").click()
fecha = datetime.now() + timedelta(2)
day = fecha.strftime('%A')
mes = fecha.month
dia_num = fecha.day
time.sleep(10)
divisions = driver.find_elements_by_class_name('scrollable')


##################################################################################

list = ["Unicos", "Primeros", "Segundos", "Guarniciones", "Postre", "Bebidas"]
Tipos = []
Unicos = []
Primeros = []
Segundos = []
Guarniciones = []
Postre = []
Bebidas = []
integer = 0

for elm in divisions:
	
	content = elm.find_elements_by_class_name('fw-700')
	category = elm.find_elements_by_css_selector("span.text-uppercase.font-14.text-green")
	Tipos = []
	if list[integer] == 'Unicos':
		for element in content:
			dish = (element.text).title()
			Unicos.append(dish)
		unicos_v = '\n'.join(Unicos) 
	elif list[integer] == 'Primeros':
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Primeros.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Primeros)]
		primeros_v = '\n'.join(total) 
	elif list[integer] == 'Segundos':
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Segundos.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Segundos)]
		segundos_v = '\n'.join(total) 
	elif list[integer] == 'Guarniciones':
		for element in content:
			dish = (element.text).title()
			Guarniciones.append(dish)
		guarniciones_v = ' | '.join(Guarniciones) 
	elif list[integer] == 'Postre':
		for element in content:
			dish = (element.text).title()
			Postre.append(dish)
		postre_v = ' | '.join(Postre) 
	elif list[integer] == 'Bebidas':
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Bebidas.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Bebidas)]
		bebidas_v = ' | '.join(total) 

	integer = integer + 1


try:


	connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
	cursor = connection.cursor()
	valor = datetime.now().strftime('%A')
	if valor in ['Thursday', 'Friday']:
		response = 'Restaurante cerrado'
		cursor.execute("INSERT INTO daily_menu (mes , dia_num, fecha, dia, unicos, primeros, segundos, guarniciones,postres, bebidas ) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)", 
		(mes, dia_num, fecha, day, response, response, response, response, response, response))
	else:
		cursor.execute("INSERT INTO daily_menu (mes , dia_num, fecha, dia, unicos, primeros, segundos, guarniciones,postres, bebidas ) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)", 
		(mes, dia_num, fecha, day, unicos_v, primeros_v, segundos_v, guarniciones_v, postre_v, bebidas_v))
	
	connection.commit()

finally:
    #closing database connection.
    if(connection):
    	cursor.close()
    	connection.close()
    	print("PostgreSQL connection is closed")

driver.quit()
