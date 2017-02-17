from pony.orm import *
from rozentools.user import *

class Juego(db.Entity):
	jugadores = Set("Jugador")
	grupo = Required(Grupo)

class Jugador(User):
	personajeAsignado = Optional(str)
	personajePropuesto = Optional(str)
	usuario = Required(User)
	juego = Required(Grupo)

db.bind('sqlite',
		'../bots.sqlite3',
		 create_db=True
		 )
db.generate_mapping(create_tables=True)
