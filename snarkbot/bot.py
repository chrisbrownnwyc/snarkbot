import os
import random
import logger
import json
import time

import conversation
import commands
import protocol as bot_protocols
import memory
from db import session, conn

from .config import max_wait_seconds,min_wait_seconds, debug, max_history_lines

class Bot(object):
	def __init__(self,botname='snarkbot',protocol='cmd'):
		self.botname = botname
		try:
			p = getattr(bot_protocols, protocol)
			self.proto = p()
		except AttributeError:
			raise ValueError("Protocol %s does not exist" % protocol)

		self.mem = memory.Memory(history=max_history_lines) # initialize memory
		self.cmd = commands.BotCtrl(botname=botname)

	def listen(self):
		try:
			randomizer = random.randint(min_wait_seconds,max_wait_seconds)
			snark_timer = int(time.time()) # checks against randomizer to know when to say something snarky
			while(True):
				response = None
				to_nick = None
				
				# cmd protocol in particular needs a timeout. We give it the randomizer so we can still get a snark
				(to_nick,_input) = self.proto.read(timeout=randomizer) 

				if _input:
					self.mem.add_history(to_nick, _input) # remember 
					response = self.cmd.parse_command(to_nick,_input,memory=self.mem)
					if response == 'shutdown':
						self.shutdown()
						break

					if not response:
				
						# get the latest conversation or create a new conversation
						c = conversation.Conversation(to_nick)
						response = c.create_response(_input)

					if response:
						snark_timer = int(time.time()) # reset the snark timer
						randomizer = random.randint(min_wait_seconds,max_wait_seconds)
				else:
					now = int(time.time())
					if (now - snark_timer) > randomizer:
						response = conversation.Snark(self.mem) # pass memory to snark so we can snark somethign based on the last input
						to_nick = 'channel'
						snark_timer = int(time.time())
						randomizer = random.randint(min_wait_seconds, max_wait_seconds)

				if response:
					self.proto.send(response,to_nick)
		except KeyboardInterrupt:
			self.shutdown()
	
	def shutdown(self):
		self.proto.send('Exiting. Good bye.','channel')
		self.proto.close()

		self.mem.commit_history() # make sure we store all the history of this session

		# close up anything in the db as well
		conn.commit()
		conn.close()
