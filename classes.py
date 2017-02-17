from pony.orm import *
from rozentools.user import *

class Juego(db.Entity):
	jugadores = Set("Jugador")
	group = Required(Group)

class Jugador(db.Entity):
	personajeAsignado = Optional(str)
	personajePropuesto = Optional(str)
	user = Required(User)
	group = Required(Group)
	juegos = Set("Juego")

db.bind('sqlite',
		'bots.sqlite3',
		 create_db=True
		 )
db.generate_mapping(create_tables=True)
