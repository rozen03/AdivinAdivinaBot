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
def newGame(user, group):
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
def startGame(group):
	juego = Juego.get(group=group)
	res = list(select(jugador.user.id_user for jugador in Jugador if jugador in juego.jugadores))
	juego.delete()
	return res
