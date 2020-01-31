

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import logging
import os
import sys
import psycopg2
from datetime import datetime, timedelta


ddbb = sys.argv[1]
column = sys.argv[2]
dia = sys.argv[3]


def query_ddbb(ddbb, column, dia): 



		fecha = datetime.now() + timedelta(7)
		day = fecha.strftime('%A')
		connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
		cursor = connection.cursor()
		#query1 = "SELECT " + column + " FROM " +  ddbb + " WHERE dia = Monday; 
		query = "SELECT primeros FROM daily_menu WHERE dia = 'Monday'"
		cursor.execute(query)
		data = cursor.fetchall()
		print (((data)))
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")


def main():

	query_ddbb('daily_menu', 'primeros', 'Monday')

if __name__ == "__main__":

	main()
