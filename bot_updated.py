

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import logging
import os
import sys
import psycopg2
from datetime import datetime, timedelta

# Enabling logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher


def query_ddbb(ddbb, column, dia): 

	data = ''
	delta = int(dia)
	try:

		fecha = datetime.now() + timedelta(delta)
		day = fecha.strftime('%A')
		day = "'" + day + "'"
		connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
		cursor = connection.cursor()
		query = "SELECT " + column + " FROM " +  ddbb + " WHERE dia = " + day + " LIMIT 1 ;"
		cursor.execute(query)
		data = cursor.fetchall()
		print (data)


	except (Exception, psycopg2.Error) as error :
		if(connection):
			print("Failed to insert record into users table", error)

	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

	return data

def start(update, context):
	logger.info("User {} started bot".format(update.effective_user["id"]))
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Prueba. Soy tu bot de Mediterránea Catering. \
		Haz click en /menu para saber que hay de comer hoy!")

def menu(update, context):
	logger.info("User {} started bot".format(update.effective_user["id"]))
	keyboard = [[InlineKeyboardButton("Ayer", callback_data='-1')], 
				[InlineKeyboardButton("Hoy", callback_data='0')], 
				[InlineKeyboardButton("Mañana", callback_data='1')]]

	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('De que día quieres saber el menu?', reply_markup=reply_markup)

def button(update, context):
	query = update.callback_query
	data = query_ddbb('daily_menu', 'primeros', query.data)
	query.edit_message_text(text=data)



def main():

	logger.info("Starting bot")

	updater.dispatcher.add_handler(CallbackQueryHandler(button))

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	start_handler = CommandHandler('menu', menu)
	dispatcher.add_handler(start_handler)

	updater.start_webhook(listen="0.0.0.0", 
						   port=PORT, 
						   url_path=TOKEN)
	updater.bot.set_webhook("https://python-telegram-endesa.herokuapp.com/" + TOKEN)
	updater.idle()


if __name__ == "__main__":

	main()



