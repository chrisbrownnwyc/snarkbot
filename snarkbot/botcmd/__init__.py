from __future__ import absolute_import
import os
import re
from dynloader import loader
import config
from . import botctrl

class BotCommand(object):
    # rules are regular expressions that point to command tokens
    # rules should be a key regular expression to a matching command
    # all input is stripped of the bot's name before checked against rules
    rules = {}

    # command tokens are individual strings that point to the code to run
    command_tokens = {}
    
    @classmethod
    def load_commands( cls, commands ):

        # get rules from all of the loaded commands
        for k,v in commands.iteritems():
            try:
                cls.rules.update(v.rules)
            except AttributeError:
                pass # no rules in this command file

            try:
                cls.command_tokens.update(v.command_tokens)
            except AttributeError:
                pass

        # botctrl overrides any custom rules
        cls.rules.update( botctrl.rules )
        cls.command_tokens.update( botctrl.command_tokens)


    @classmethod
    def parse_command(cls,nick, msg):

        # see if we have a command
        for k,v in cls.rules:
            m = re.search(k, msg):
            if m:
                try:
                    (instcls,method) = cls.command_tokens[v]
                    cmd = instcls()
                    args = list(m.groups())
                    return getattr(cmd,method)(nick, *args)
                except (KeyError, AttributeError):
                    return False

        return False


# hack to get all the command plugins dynamically
importpath = os.path.dirname(os.path.abspath(__file__))
# import paths from configs as well
paths = []

try:
    if config.extra_command_paths:
        paths.extend(config.extra_command_paths)
except AttributeError:
    pass

paths.append(importpath)

commands = {} 
for p in paths:
    commands.update(loader(p, BotCommand))

BotCommand.load_commands(commands)
