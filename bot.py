

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

def query_ddbb(): 
	try:

	    connection = psycopg2.connect(user = "lstzeuvfrgwgva",
	                                  password = "705cba1d67eefffd029de6bb3f7e1dfdd2b9f83cf8711d6bfb466e734c545a6d",
	                                  host = "ec2-54-75-249-16.eu-west-1.compute.amazonaws.com",
	                                  port = "5432",
	                                  database = "d9iffrf6gikj6a")

	    cursor = connection.cursor()
	    cursor.execute("SELECT OCCUPANCY FROM users_check ORDER BY id DESC LIMIT 1;")
	    occupancy = cursor.fetchall()


	except (Exception, psycopg2.Error) as error :
		if(connection):
			print("Failed to insert record into users table", error)

	finally:
		#closing database connection.
		if(connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")

	return occupancy

def start_handler(update, context):

	logger.info("User {} started bot".format(update.effective_user["id"]))
	update.message.reply_text("Hola eduardocampillosgarcia! Soy tu bot de Mediterránea Catering. Haz click en /menu para saber que hay de comer hoy!")

def menu(update, context):

	context.bot.send_message(chat_id=update.effective_chat.id, text="Este es el menu de hoy. LINK: http://endesa.med-menuonline.com/")
	context.bot.send_document(chat_id=update.effective_chat.id, document=open('./' + context.args[0] + '.pdf', 'rb'))

def occupancy(update, context):

	rate_occupancy = query_ddbb();
	update.message.reply_text(rate_occupancy);


def main():

	logger.info("Starting bot")

	updater = Updater(TOKEN, use_context=True)

	updater.dispatcher.add_handler(CommandHandler("start", start_handler))
	updater.dispatcher.add_handler(CommandHandler("menu", menu, pass_args = True)) 
	updater.dispatcher.add_handler(CommandHandler("occupancy", occupancy, pass_args=False))

	updater.start_webhook(listen="0.0.0.0", 
						   port=PORT, 
						   url_path=TOKEN)
	updater.bot.set_webhook("https://python-telegram-endesa.herokuapp.com/" + TOKEN)
	updater.idle()


if __name__ == "__main__":

	main()



