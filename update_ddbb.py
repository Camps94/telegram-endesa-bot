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
time.sleep(10)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/button[6]").click()
fecha = datetime.now() + timedelta(5)
day = fecha.strftime('%A')
time.sleep(15)
divisions = driver.find_elements_by_class_name('scrollable')


##################################################################################

list = ["Unicos", "Primeros", "Segundos", "Guarniciones", "Postre", "Bebidas"]
Unicos = []
Primeros = []
Segundos = []
Guarniciones = []
Postre = []
Bebidas = []
integer = 0


for elm in divisions:
	content = elm.find_elements_by_class_name('fw-700')
	if list[integer] == 'Unicos':
		for element in content:
			Unicos.append(element.text)
	elif list[integer] == 'Primeros':
		for element in content:
			Primeros.append(element.text)
	elif list[integer] == 'Segundos':
		for element in content:
			Segundos.append(element.text)
	elif list[integer] == 'Guarniciones':
		for element in content:
			Guarniciones.append(element.text)
	elif list[integer] == 'Postre':
		for element in content:
			Postre.append(element.text)
	elif list[integer] == 'Bebidas':
		for element in content:
			Bebidas.append(element.text)

	integer = integer + 1

unicos_v = "|"
unicos_v = unicos_v.join(Unicos)  
primeros_v = "|"
primeros_v = primeros_v.join(Primeros) 
segundos_v = "|"
segundos_v = segundos_v.join(Segundos) 
guarniciones_v = "|"
guarniciones_v = guarniciones_v.join(Guarniciones) 
postre_v = "|"
postre_v = postre_v.join(Postre) 
bebidas_v = "|"
bebidas_v = bebidas_v.join(Bebidas)

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
