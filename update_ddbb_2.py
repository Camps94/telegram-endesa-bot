#!/usr/local/opt/python/libexec/bin/python

from selenium import webdriver
import time
import sqlite3
from datetime import datetime, timedelta
import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging
import os
import sys

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
link = 'https://mediterranea.online/client/courses'
driver.get(link)

driver.find_element_by_id('email').send_keys('eduardo.garcia2@enel.com')
driver.find_element_by_id('password').send_keys("123456")
driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/div[3]/button").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/ul/li[4]/button").click()
time.sleep(15)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/button[1]").click()
fecha = datetime.now() + timedelta(0)
day = fecha.strftime('%A')
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
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Unicos.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Unicos)]
		unicos_v = '  '.join(total) 
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
		segundos_v = ' | '.join(total) 
	elif list[integer] == 'Guarniciones':
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Guarniciones.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Guarniciones)]
		guarniciones_v = ' | '.join(total) 
	elif list[integer] == 'Postre':
		for cat in category:
			catg = cat.text
			Tipos.append(catg)
		for element in content:
			dish = (element.text).title()
			Postre.append(dish)
		total = [ x + ': ' + y for x, y in zip(Tipos, Postre)]
		postre_v = ' | '.join(total) 
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
	cursor.execute("INSERT INTO daily_menu (fecha, dia, unicos, primeros, segundos, guarniciones,postres, bebidas ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", 
		(fecha, day, unicos_v, primeros_v, segundos_v, guarniciones_v, postre_v, bebidas_v))
	connection.commit()


finally:
    #closing database connection.
    if(connection):
    	cursor.close()
    	connection.close()
    	print("PostgreSQL connection is closed")

driver.quit()
