from db import conn, session
from datetime import datetime
from uuid import uuid4

class PhraseNotFound(Exception):
	pass

class ResponseNotFound(Exception):
	pass

# just a wrapper around some common operations in sql
class Memory(object):
	def __init__(self,history=50):
		self.history_max_lines = int(history)

		# init history
		session.execute('SELECT * FROM history LIMIT %d ORDER BY added DESC', self.history_max_lines)
		self.history = session.fetchall().reverse() # reverse so we can append rather than insert

	def get_phrase(self,phrase_id):
		session.execute("SELECT * FROM phrase WHERE id=?",[phrase_id])
		return self.zip_phrase(session.fetchone())

	def get_phrase_by_text(self,text):
		session.execute("SELECT * FROM phrase WHERE phrase=?",[text])
		return self.zip_phrase(session.fetchone())

	def zip_phrase(self,phrase):
		if phrase:
			return dict(zip(['id','added','phrase','added_by'],[phrase]))
		else:
			return None

	def get_response(self,response_id):
		session.execute("SELECT * FROM response WHERE response_id=?",[response_id])
		return self.zip_response(session.fetchone())

	def get_response_by_text(self,text,phrase_id):
		session.execute("SELECT * FROM response WHERE response=? AND phrase_id=?",[text,phrase_id])
		return self.zip_response(session.fetchone())

	def zip_response(self,response):
		if response:
			return dict(zip(['id','phrase_id','response','added','added_by'],response) )
		else:
			return None
		
	def remember(self,keyvalue,response,added_by):
		phrase = self.get_phrase_by_text(keyvalue)
		try:
			phrase_id = phrase['id']
			# we have this phrase, check if we already have this response
			response = self.get_response_by_text(response, phrase_id)
			try:
				response_id = responses['id']
				return response_id
			except (AttributeError,KeyError):
				pass

		except (AttributeError,KeyError):
			phrase_id = str(uuid4())
			session.execute("INSERT INTO phrase (id,added,phrase,added_by) VALUES(?,?,?,?)",
				[phrase_id, datetime.now().isoformat(), keyvalue, added_by.name]
				)

		# insert the response
		response_id = str(uuid4())
		session.execute("INSERT INTO responses(id,phrase_id,response,added,added_by) VALUES(?,?,?,?,?)",
			[response_id, phrase_id, response, datetime.now().isoformat(), added_by.name]
			)
		return response_id


	def forget_response(self,keyvalue,response):
		phrase = self.get_phrase_by_text(keyvalue)
		try:
			response = self.get_response_by_text(response, phrase['id'])
			try:
				response_id = response['id']
				session.execute('DELETE FROM responses WHERE id=?',[response_id])
				conn.commit()
			except (AttributeError,KeyError):
				raise ResponseNotFound('That response does not exist')

		except (AttributeError,KeyError):
			raise PhraseNotFound('That phrase does not exist')

	def forget_all(self,keyvalue):
		phrase = self.get_phrase_by_text(keyvalue)

		try:
			session.execute('DELETE FROM responses WHERE phrase_id=?',[phrase['id']])
			session.execute('DELETE FROM phrase WHERE phrase_id=?',[phrase['id']] )
			conn.commit()
		except (AttributeError,KeyError):
			raise PhraseNotFound('That phrase does not exist')

		return True

	def add_history(self, nick, history_line ):
		if len(self.history) > self.history_max_lines:
			del self.history[0]

		self.history.append([nick,history_line, datetime.isoformat()])
		
	def commit_history(self):
		# first delete any old stored history
		# note that if the max lines config variable is shortened that some history will hang around
		# I don't see this as a huge problem
		session.execute('DELETE FROM history LIMIT %d' % len(self.history) )

		# now insert everything we have stored so far
		session.executemany( 'INSERT INTO history VALUES (?,?,?)', self.history)
		conn.commit()

	def recall_history(self,lines=1):
		# get lines number of lines of previous history
		start = len(self.history) - lines
		if start < 0:
			start = 0

		hslice = self.history[start:len(self.history)]
		return hslice

	def find_history_by_nick(self,nick,lines=1):
		# find the last lines said by [nick]

		rhistory = self.history.reverse()
		nicklines = []
		for h in rhistory:
			if h[0] == nick:
				nicklines.append(h)

			if len(nicklines) == lines:
				break

		return nicklines

	def find_history_by_phrase(self,phrase,lines=1):
		# find the last thing said that matches the phrase (uses "in")
		rhistory = self.history.reverse()
		phraselines = []
		for h in rhistory:
			if phrase in h[1]:
				phraselines.append(h)

			if len(phraselines) == lines:
				break

		return phraselines
