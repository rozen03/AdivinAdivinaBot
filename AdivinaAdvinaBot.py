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
def start(bot, update):
	registrar(bot, update)
	update.message.reply_text(text="Holas, soy el AdivinaAdivinaBot, Por que no te vas a la mierda? :D",quote=False)

def button(bot, update):
    query = update.callback_query #toma la informacion del boton que se apreto
    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)#edita el mensaje usando la informacion que le llego del boton

#----------------------------------------------------------------------------------------------------------------------------------------------

@db_session
def join(user, group):
	jugador = Jugador.get(user=user,group=group)
	res = NOTHING
	if (not jugador):
		jugador = Jugador(user=user,group=group)
	juego = Juego.get(group=group)
	if (jugador not in juego.jugadores):
		juego.jugadores.add(jugador)
		res = JOINED
	return res
@db_session
def startGame(user, group):
	juego = Juego.get(group=group)
	res = NOTHING
	if (not juego ):
		juego = Juego(group=group)
		res=STARTED
	commit()
	resTwo=join(user, group)
	if(res == NOTHING):
		res= resTwo
	return res

@db_session
def startGame_command(bot,update):
	user, group = registrar(bot, update)
	res = startGame(user,group)
	text=""
	if(res ==NOTHING):
		text= "Ya hay un juego creado y estás adentro, IDIOTA!"
	else:
		if(res==STARTED):
			text="Una nueva partida ha sido creada, pone /join para unirte.\n"
		text+=user.first_name+" "+user.last_name+ " se ha unido a la partida."
	responder(bot,update,text)
@db_session
def join_command(bot,update):
	user, group = registrar(bot, update)
	res = join(user,group)
	text=""
	if(res ==NOTHING):
		text= "Ya hay un juego creado y estás adentro, IDIOTA! ... o no hay un juego creado XD"
	else:
		text=user.first_name+" "+user.last_name+ " se ha unido a la partida."
	responder(bot,update,text)

#NOTA: Desde esta parte del codigo no le den mucha bola si quieren, esto inicializa un monton de cosas
def main():
	global update_id
	try:
		loguear("Iniciando AdivinaAdivinaBot")
		print("Iniciando AdivinaAdivinaBot",end="...")
		botname = "AdivinaAdivinaBot"
		# Telegram Bot Authorization Token
		updater = Updater(token=AdivinaAdivinaBottookn)
		dispatcher = updater.dispatcher
		j = updater.job_queue
		start_handler = CommandHandler('start', start)
		dispatcher.add_handler(start_handler)


		#comandos = [('buttonz', buttonz),('startGame',startGame),('join',join),('begin',begin)]
		comandos=[("startGame", startGame_command),("join",join_command)]
		comandosArg=[]
		#comandosArg = [('tuvieja', tuvieja), ('repetime',repetime)]
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
		print("ERROR AL INICIAR EL AdivinaAdivinaBot")
		loguear("ERROR AL INICIAR EL AdivinaAdivinaBot")
		result = str(type(inst)) + "\n"    	# the exception instance
		result += str(inst.args) + "\n"     # arguments stored in .args
		# __str__ allows args to be printed directly,
		result += str(inst) + "\n"
		loguear(result)
		print(result)

if __name__ == '__main__':
    main()
