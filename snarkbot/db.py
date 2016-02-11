import os
import sqlite3
from .config import dbfile
from uuid import uuid4

# sets up a session (cursor) and creates the bot memory if it doesn't exist

conn = sqlite3.connect(dbfile)
session = conn.cursor()

def has_table(table):
	session.execute("SELECT name FROM sqlite_master WHERE type='table' and name=?", [table])
	tbl = session.fetchone()
	if tbl:
		return True

	return False

nc = False

if not has_table('phrase'):
	session.execute("CREATE TABLE phrase (id text, added text, phrase text, added_by text)")
	nc = True

if not has_table('responses'):
	session.execute("CREATE TABLE responses(id text, phrase_id text, response text, added text, added_by text)")
	nc = True

if not has_table('bucket'):
	session.execute("CREATE TABLE bucket(id text, thing text, added text, added_by text)")
	nc = True

if not has_table('conversation'):
	session.execute("CREATE TABLE conversation(id text, with text, context blob)")
	nc = True

if not has_table('nick'):
	session.execute("CREATE TABLE nick(name text, privileged integer,added text)")
	nc = True

if not has_table('history'):
	session.execute('CREATE TABLE history(nick text,line text,added text)')
	nc = True

if nc:
	conn.commit()
