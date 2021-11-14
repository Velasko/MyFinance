from .session import SessionManager
from .scheme import *

def list_tables():
	pass

def create_database():
	engine = create_engine(user_variables+path)
	Base.metadata.create_all(engine)

def authenticate():
	if db_created:
		engine = create_engine(user_variables+path)
		Base.metadata.bind = engine
		return SessionManager(engine)