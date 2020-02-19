

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import telegram.ext
import requests
import logging
import os
import sys
import psycopg2
from datetime import datetime, timedelta, time



# Enabling logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue

def query_ddbb(ddbb, dia): 

	data = []
	delta = int(dia)
	try:

		fecha = datetime.now() + timedelta(delta)
		mes = fecha.month
		dia_num = fecha.day
		day = fecha.strftime('%A')
		day = "'" + day + "'"
		connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")
		cursor = connection.cursor()
		#query = "SELECT " + "primeros, segundos, unicos, guarniciones, postres" + " FROM " +  ddbb + " WHERE dia = " + day + " ORDER BY fecha  DESC LIMIT 1 ;"
		
		query = """"SELECT primeros, segundos, unicos, guarniciones, postres FROM {ddbb} WHERE dia = {day}
				AND dia_num = {dia_num}""".format(ddbb=ddbb, dia=day, dia_num = dia_num)

		cursor.execute(query)
		data = cursor.fetchall()
		print(data)

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
	name = update.effective_user["first_name"] or update.effective_user["username"]
	context.bot.send_message(chat_id=update.effective_chat.id, text="Hola {}! Soy el bot del Catering de Endesa. \
		Haz click en /menu para saber que hay de comer hoy o mañana!".format(name))



def menu(update, context):
	logger.info("User {} started bot".format(update.effective_user["id"]))
	keyboard = [[InlineKeyboardButton("Ayer", callback_data='-1')], 
				[InlineKeyboardButton("Hoy", callback_data='0')], 
				[InlineKeyboardButton("Mañana", callback_data='1')]]

	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('De que día quieres saber el menu?', reply_markup=reply_markup)

def button(update, context):
	query = update.callback_query
	data = query_ddbb('daily_menu', query.data)
	delta = int(query.data)
	fecha = datetime.now() + timedelta(delta)
	mes = fecha.month
	dia_num = fecha.day



	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="Menu del día: {dia_num}/{mes}/2020".format(dia_num=dia_num, mes=mes))
	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="__*PRIMEROS fsdf \n Hola*__")
	context.bot.send_message(chat_id=update.effective_chat.id, text=data[0][0])
	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="__*SEGUNDOS*__")
	context.bot.send_message(chat_id=update.effective_chat.id, text=data[0][1])
	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="__*ÚNICOS*__")
	context.bot.send_message(chat_id=update.effective_chat.id, text=data[0][2])
	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="__*GUARNICIONES*__")
	context.bot.send_message(chat_id=update.effective_chat.id, text=data[0][3])
	context.bot.send_message(chat_id=update.effective_chat.id, parse_mode = 'MarkdownV2',  text="__*POSTRES*__")
	context.bot.send_message(chat_id=update.effective_chat.id, text=data[0][4])

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Lo siento pero no te entendí. Haz click en /menu para conocer el menu de hoy")


def main():

	logger.info("Starting bot")

	updater.dispatcher.add_handler(CallbackQueryHandler(button))

	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)

	start_handler = CommandHandler('menu', menu)
	dispatcher.add_handler(start_handler)

	unknown_handler = MessageHandler(Filters.command, unknown)
	dispatcher.add_handler(unknown_handler)

	unknown_handler2 = MessageHandler(Filters.text, unknown)
	dispatcher.add_handler(unknown_handler2)


	updater.start_webhook(listen="0.0.0.0", 
						   port=PORT, 
						   url_path=TOKEN)
	updater.bot.set_webhook("https://python-telegram-endesa.herokuapp.com/" + TOKEN)
	updater.idle()


if __name__ == "__main__":

	main()



