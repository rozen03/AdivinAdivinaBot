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

def start(bot, update):
	registrar(bot, update)
	update.message.reply_text(text="Holas, soy el AdivinaAdivinaBot, Por que no te vas a la mierda? :D",quote=False)

def buttonz(bot, update):
	registrar(bot, update)
	keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(
        text="Please choose:",
        reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def tuvieja(bot, update, groups):
	registrar(bot, update)
	update.message.reply_text(
            text="[Rozen](telegram.me/Rozzen)",
            disable_web_page_preview=True,
            parse_mode=telegram.ParseMode.MARKDOWN)

def repetime(bot, update, groups):
	registrar(bot, update)
	texto=groups[1]
	update.message.reply_text( text=texto)
global estoEsUnBool
estoEsUnBool=False
def decirCosa(bot,job):
	global estoEsUnBool
	chat_id, texto = job.context.split("|",1)
	bot.sendMessage(chat_id=int(chat_id), text=texto)
	if(estoEsUnBool):
		job.schedule_removal()
	else:
		estoEsUnBool=True
def decimeEnSegundos(bot, update, groups,job_queue):
	global estoEsUnBool
	registrar(bot, update)
	texto=groups[1]
	try:
		iniciarEn, repetirEn, texto = texto.split(" ",2)
		iniciarEn=int(iniciarEn)
		repetirEn=int(repetirEn)
		job = Job(decirCosa, repetirEn, repeat=True, context=str(update.message.chat_id)+"|"+texto)
		job_queue.put(job, next_t=iniciarEn)
		estoEsUnBool=False
	except Exception as inst:
		print(inst)
		responder(bot,update,text="Pusiste algo mal")

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

		comandos = [('buttonz', buttonz)]
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
