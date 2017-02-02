#2.Etapa de asignacion de personajes
#Juego

def validar(personajes, personajesPorUsuario):
	for indice,valor in enumerate(personajesPorUsuario.values()):
		if(personajes[indice] == valor):
			return False
	return True


def foo(juego):
	personajesPorUsuario = juego.personajePorUsuario
	personajes = list(personajesPorUsuario.values())
	shuffle(personajes)
	while(not validar(personajes,personajesPorUsuario)):
		shuffle(personajes)
	i=0
	for jugador in juego.jugadores.values():
		jugador.personaje = personaje[i]
		i+=1

	for jugador in juego.jugadores.values():
		personajesDeLosDemas= [jugador.first_name+ " "+jugador.last_name+": "+ jugadorsin.personaje \
				for indice, jugadorsin in juego.jugadores.items() if indice != jugador.indice]
		textoAEnviar = str.join("\n",personajesDeLosDemas)
		mandarMensaje(jugador,"Los personajes del resto de los jugadores son \n"+textoAEnviar)
