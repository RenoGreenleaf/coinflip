# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(create_engine('sqlite:///db.sqlite3'))
