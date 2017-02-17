from pony.orm import *
from rozentools.user import *

class Juego(db.Entity):
	jugadores = Set("Jugador")
	grupo = Required(Grupo)

class Jugador(User):
	personajeAsignado = Optional(str)
	personajePropuesto = Optional(str)
	user = Required(User)
