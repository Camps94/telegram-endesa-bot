

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram.ext
import requests
import logging
import os
import sys
import psycopg2
from datetime import datetime, timedelta, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
import os
from bot import query_ddbb

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue

def send_reminder(chat_id):
	data = query_ddbb('daily_menu', '0')
	#chat_id=update.effective_chat.id
	fecha = datetime.now() 
	mes = fecha.month
	dia_num = fecha.day
	day = fecha.strftime('%A')
	if day in ['Saturday', 'Sunday']:
		text="Menu del día: {dia_num}/{mes}/2020".format(dia_num=dia_num, mes=mes)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + text
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "*Restaurance: Cerrado*"
		response = requests.get(send_text)
	else:
		text="Menu del día: {dia_num}/{mes}/2020".format(dia_num=dia_num, mes=mes)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + text
		response = requests.get(send_text)

		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "_*PRIMEROS*_"
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + data[0][0]
		response = requests.get(send_text)

		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "_*SEGUNDOS*_"
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + data[0][1]
		response = requests.get(send_text)

		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "_*ÚNICOS*_"
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + data[0][2]
		response = requests.get(send_text)

		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "_*GUARNICIONES*_"
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + data[0][3]
		response = requests.get(send_text)

		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + "_*POSTRES*_"
		response = requests.get(send_text)
		send_text = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + chat_id + '&parse_mode=MarkdownV2&text=' + data[0][4]
		response = requests.get(send_text)


def main():

	logger.info("Starting bot")

	try:
		password_ddbb = os.getenv("PASSWORD_DATABASE")
		connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = password_ddbb,
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
		cursor = connection.cursor()
		query = """SELECT user_id FROM {ddbb}  WHERE status = {status} ;""".format(ddbb='notifications', status = "'ON'")
		cursor.execute(query)
		user_id = cursor.fetchall()
		print (user_id)

	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

	for user in user_id:
		send_reminder(user[0])

if __name__ == "__main__":

	main()
