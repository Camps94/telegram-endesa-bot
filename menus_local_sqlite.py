#!/usr/local/opt/python/libexec/bin/python

from selenium import webdriver
import time
import sqlite3
from datetime import datetime, timedelta

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
link = 'https://mediterranea.online/client/courses'
driver.get(link)

driver.find_element_by_id('email').send_keys('eduardo.garcia2@enel.com')
driver.find_element_by_id('password').send_keys("123456")
driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/form/div[3]/button").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/ul/li[4]/button").click()
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/button[6]").click()
fecha = datetime.now() + timedelta(7)
day = fecha.strftime('%A')
time.sleep(5)
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


	conn = sqlite3.connect('menu.db')
	c = conn.cursor()
	c.execute("INSERT INTO daily_menu (fecha, dia, unicos, primeros, segundos, guarniciones,postres, bebidas ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
		(fecha, day, unicos_v, primeros_v, segundos_v, guarniciones_v, postre_v, bebidas_v))
	conn.commit()


finally:
    #closing database connection.
    if(conn):
    	c.close()
    	conn.close()
    	print("PostgreSQL connection is closed")

driver.quit()
