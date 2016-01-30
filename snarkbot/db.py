import os
import sqlite3
from .config import dbfile
from uuid import uuid4

# sets up a session (cursor) and creates the bot memory if it doesn't exist

conn = sqlite3.connect(dbfile)
session = conn.cursor()
if not os.path.exists(dbfile):
	session.execute('''CREATE TABLE phrase (id text, added text, phrase text, added_by text)''')
	session.execute('''CREATE TABLE responses(id text, phrase_id text, response text, added text, added_by text)''')
	session.execute('''CREATE TABLE bucket(id text, thing text, added text, added_by text)''')
	session.execute('''CREATE TABLE conversation(id text, with text, context blob)''')

	conn.commit()
