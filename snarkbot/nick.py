# handles "nicks" (users) and their privileges
from .db import conn,session
from datetime import datetime

class NickNotFound(Exception):
	pass

class NickExists(Exception):
	pass

class NickMemory(object):
	def get_nick(self,name):
		session.execute("SELECT * FROM nick WHERE name=?",[nick])
		return self.zip_nick(session.fetchone())

	def zip_nick(self,nick):
		if nick:
			return dict(zip(['name,privileged,added'], nick) )
		else:
			raise NickNotFound('Did not found the specified name')

	def forget_nick(self,name):
		session.execute('DELETE FROM nick WHERE name=?',[nick])
		conn.commit()

	def add_nick(self,name):
		try:
			existing = self.get_nick(name)
			raise NickExists('That name already exists')
		except NickNotFound:
			nick_values = [name, 0, datetime.now().isoformat()]
			session.execute('INSERT INTO nick(name,privileged,added) VALUES (?,?,?)',
				)
			conn.commit()
			return self.zip_nick(nick_values)

	def set_privilege(self,nick,priv):
		nick = self.get_nick(name)
		session.execute('UPDATE nick SET privileged=1 WHERE name=?',[name,priv])
		conn.commit()
		
	def promote_nick(self,name):
		self.set_privilege(name,1)
		
	def demote_nick(self,name):
		self.set_privilege(name,0)

class Nick(object):
	def __init__(self,name=name):
		try:
			nick_dict = NickMemory().get_nick(name)
		except NickNotFound:
			nick_dict = NickMemory().add_nick(name)

		self.name = nick_dict.get('name')
		self.added = nick_dict.get('added')
		self.privileged = nick_dict.get('privileged')

	def is_privileged(self):
		return self.privileged

	def promote(self):
		NickMemory().promote_nick(self.name)

	def demote(self):
		NickMemory().demote_nick(self.name)
