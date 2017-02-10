@db_session
def join(bot, update):
	usuario, grupo = registrar(bot, update)
	jugador = Jugador.get(user=usuario,grupo=grupo)
	if (jugador is None):
		jugador = Jugador(usuario=usuario,grupo=grupo)
	juego = Juego.get(grupo=grupo)
	if (jugador not in juego.jugadores)	
		juego.jugadores.add(jugador)
def iniciarJuego(bot,update):
	usuario, grupo = registrar(bot, update)
	juego = Juego.get(grupo=grupo)
	if (juego is None):
		juego = Juego(grupo=grupo)
	join(bot, update)
	