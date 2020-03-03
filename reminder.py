

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
	logger.info("User {} started bot".format(update.effective_user["id"]))
	data = query_ddbb('daily_menu', '0')
	#chat_id=update.effective_chat.id
	fecha = datetime.now() 
	mes = fecha.month
	dia_num = fecha.day
	day = fecha.strftime('%A')
	if day in ['Saturday', 'Sunday']:
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="Menu del día: {dia_num}/{mes}/2020".format(dia_num=dia_num, mes=mes))
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="*Restaurance: Cerrado*")
	else:
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="Menu del día: {dia_num}/{mes}/2020".format(dia_num=dia_num, mes=mes))
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="_*PRIMEROS*_")
		context.bot.send_message(chat_id=chat_id, text=data[0][0])
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="_*SEGUNDOS*_")
		context.bot.send_message(chat_id=chat_id, text=data[0][1])
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="_*ÚNICOS*_")
		context.bot.send_message(chat_id=chat_id, text=data[0][2])
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="_*GUARNICIONES*_")
		context.bot.send_message(chat_id=chat_id, text=data[0][3])
		context.bot.send_message(chat_id=chat_id, parse_mode = 'MarkdownV2',  text="_*POSTRES*_")
		context.bot.send_message(chat_id=chat_id, text=data[0][4])

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
		query = """SELECT user_id FROM {ddbb}  WHERE status = {status} ;""".format(ddbb='notifications', status = 'ON')
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

	updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
	updater.bot.set_webhook("https://python-telegram-endesa.herokuapp.com/" + TOKEN)
	updater.idle()


if __name__ == "__main__":

	main()
