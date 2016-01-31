import os
from .dynloader import loader
from .config import extra_command_paths

# hack to get all the command plugins dynamically
importpath = os.path.dirname(os.path.abspath(__file__))
# import paths from configs as well
paths = extra_command_paths
paths.append(importpath)

commands = {} 
for p in paths:
	commands.update(loader(p, 'SnarkbotCommand'))

# rules are regular expressions that point to command tokens
# rules should be a tuple, pattern, token
# all input is stripped of the bot's name before checked against rules
rules = []

# command tokens are individual strings that point to the code to run
command_tokens = {}

# get rules from all of the loaded commands
for k,v in commands.iteritems():
	try:
		rules.append( v.rules ) # rules should be a static dict for each command but they don't have to be there
	except AttributeError:
		pass

# set local rules
rules.append( '^shutdown','shutdown' )
rules.append( '^promote ([^\s]+)$','promote')
rules.append( '^demote ([^\s]+)$','demote')

command_tokens['shutdown'] = BotCtrl.shutdown # I don't want to call this statically so this might not work.
command_tokens['promote'] = BotCtrl.promote
command_tokens['demote'] = BotCtrl.demote

class BotCtrl(object):
	def __init__(self,botname=botname):
		self.botname = botname

	def parse_command(nick, msg,memory=None):
		# see if we have a command
		parts = msg.split(' ')
		try:
			if not parts[0].startswith('_') and parts[0] != 'parse_command':
				cmd = getattr(self,parts[0].strip())
				try:
					args = parts[1:]
				except IndexError:
					args = []
			
				cmd(self, nick, *args)
			else:
				return False
		except(IndexError,AttributeError):
			# Standback! I know regular expressions!


			return False # isn't a command

	
	# below are all commands. Commands require the nick as the first argument
	
	# admin commands
	def shutdown(self,nick,*args):
		if nick in self.priv:
			return 'shutdown'

		return self.unauthorized(nick)

	def promote(self,nick,*args):
		if nick in self.priv:
			try:
				pnick = args[0]
				try:
					privileged.add_admin(pnick)
					return 'Added bot wrangler %s' % pnick
				except privileged.AdminExists:
					return '%s is already a bot wrangler.' % pnick

			except IndexError:
				return 'Sorry but I need a name to promote'

		return self.unauthorized(nick)

	def demote(self,nick,*args):
		if nick in self.priv:
			try:
				pnick = args[0]
				try:
					privileged.delete_admin(pnick)
					return 'Removed %s as a bot wrangler.' % pnick
				except privileged.AdminNotFound:
					return '%s is not a bot wrangler.' % pnick
			except IndexError:
				return 'Sorry but I need a name to demote.'
		else:
			return self.unauthorized(nick)

	def _unauthorized(self, nick):
		return 'I can\'t let you do that %s' % nick

	# fun things anyone can do
	def give(self,nick,*args):
		pass

	def drop(self,nick,*args):
		pass
		
	def remember(self,nick,*args):
		pass

	def forget(self,nick,*args):
		pass

	def diceroll(self,nick,*args):
		pass

	def magic8ball(self,nick,*args):
		pass

	def calc(self,nick,*args):
		pass

	def xkcd(self,nick,*args):
		pass

	def google(self,nick,*args):
		pass
