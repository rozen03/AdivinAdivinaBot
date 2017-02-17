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
def join(usuario, grupo):
	usuario, grupo = registrar(bot, update)
	jugador = Jugador.get(user=usuario,grupo=grupo)
	res = NOTHING
	if (jugador is None):
		jugador = Jugador(usuario=usuario,grupo=grupo)
	juego = Juego.get(grupo=grupo)
	if (jugador not in juego.jugadores)
		juego.jugadores.add(jugador)
		res = JOINED
	return res
@db_session
def startGame(usuario, grupo):
	juego = Juego.get(grupo=grupo)
	res = NOTHING
	if (juego is None):
		juego = Juego(grupo=grupo)
		res=STARTED
	resTwo=join(usuario, grupo)
	if(res == NOTHING):
		res= resTwo
	return res

def startGame(bot,update):
	user, group = registrar(bot, update)


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
		handlr = RegexHandler("^(?i)/decimeEnSegundos(|@" + botname + ")\s(.*)",
        		decimeEnSegundos,
        		pass_groups=True,
        		pass_groupdict=False,
        		pass_update_queue=False,
        		pass_job_queue=True)
		dispatcher.add_handler(handlr)

		comandos = [('buttonz', buttonz),('startGame',startGame),('join',join),('begin',begin)]
		comandosArg = [('tuvieja', tuvieja), ('repetime',repetime)]
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
