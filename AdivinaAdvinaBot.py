#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep
from telegram.ext import Job
from rozentools.commontools import *
from rozentools.errortools import *
from tookns import AdivinaAdivinaBottookn
from random import shuffle
from defines import *
from classes import *
from game	import *
def start(bot, update):
	registrar(bot, update)
	update.message.reply_text(text="Holas, soy el AdivinaAdivinaBot, Por que no te vas a la mierda? :D",quote=False)

def button(bot, update):
    query = update.callback_query #toma la informacion del boton que se apreto
    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)#edita el mensaje usando la informacion que le llego del boton

#----------------------------------------------------------------------------------------------------------------------------------------------


def newGame_command(bot,update):
	with db_session:
		user, group = registrar(bot, update)
		res = newGame(user,group)
		text=""
		if(res ==NOTHING):
			text= "Ya hay un juego creado y ya estas adentro, IDIOTA!"
		else:
			if(res==STARTED):
				text="Una nueva partida ha sido creada, pone /join para unirte\n"
			text+=user.first_name+" "+user.last_name+ "se ha unido a la partida"
	responder(bot,update,text)

def join_command(bot,update):
	with db_session:
		user, group = registrar(bot, update)
		res = join(user,group)
		text=""
		if(res ==NOTHING):
			text= "Ya hay un juego creado  y ya estas adentro, IDIOTA! ... o no hay un juego creado xD"
		else:
			text=user.first_name+" "+user.last_name+ "se ha unido a la partida"
	responder(bot,update,text)

def startGame_command(bot,update):
	with db_session:
		user, group = registrar(bot, update)
		usersId= startGame(group)
	for userId in usersId:
		mandarMensaje(bot,userId, "Eh wacho tirame la palabra (Pero no te voy a responder nada ni hacer nada con eso, MWAHAHA)")



#NOTA: Desde esta parte del codigo no le den mucha bola si quieren, esto inicializa un monton de cosas
def main():
	global update_id
	try:
		loguear("Iniciando AdivinAdivinaBot")
		print("Iniciando AdivinAdivinaBot",end="...")
		botname = "AdivinAdivinaBot"
		# Telegram Bot Authorization Token
		updater = Updater(token=AdivinaAdivinaBottookn)
		dispatcher = updater.dispatcher
		j = updater.job_queue
		start_handler = CommandHandler('start', start)
		dispatcher.add_handler(start_handler)
		comandos=[("newGame", newGame_command),("join",join_command),("startGame", startGame_command),]
		comandosArg=[]
		for c in comandos:
			handlearUpperLower(c[0], c[1], dispatcher, botname)
		for c in comandosArg:
			handlearUpperLowerArgs(c[0], c[1], dispatcher, botname)
		handlearCommons(dispatcher, botname)
		handlearErrors(dispatcher, botname)
		handler = MessageHandler(Filters.text | Filters.command, registrar)
		dispatcher.add_handler(handler)
		dispatcher.add_handler(CallbackQueryHandler(button))
		dispatcher.add_handler(MessageHandler(Filters.status_update,registrarIO))
		#job_minute = Job(callback_minute, 1800.0)
		#j.put(job_minute, next_t=0.0)
		#updater.start_polling()
		updater.start_polling(clean=True)
		print("OK")
	except Exception as inst:
		print("FAIL")
		print("ERROR AL INICIAR EL AdivinAdivinaBot")
		loguear("ERROR AL INICIAR EL AdivinAdivinaBot")
		result = str(type(inst)) + "\n"    	# the exception instance
		result += str(inst.args) + "\n"     # arguments stored in .args
		# __str__ allows args to be printed directly,
		result += str(inst) + "\n"
		loguear(result)
		print(result)

if __name__ == '__main__':
    main()
