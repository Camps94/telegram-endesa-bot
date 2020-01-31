

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging
import os
import sys
import psycopg2

# Enabling logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))

 
try:

	connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
	query = """CREATE TABLE "daily_menu" (
	"fecha"	TEXT DEFAULT '30-01-2020',
	"dia"	TEXT DEFAULT 'None',
	"primeros"	TEXT DEFAULT 'None',
	"segundos"	TEXT DEFAULT 'None',
	"guarniciones"	TEXT DEFAULT 'None',
	"unicos"	TEXT DEFAULT 'None',
	"postres"	TEXT DEFAULT 'None',
	"bebidas"	TEXT DEFAULT 'None'
); """
	cursor = connection.cursor()
	cursor.execute(query)
	connection.commit()

finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")









