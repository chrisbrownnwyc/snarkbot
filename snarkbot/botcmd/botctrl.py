from . import bot

class BotCtrl(object):
    # below are all commands. Commands require the nick as the first argument
    
    # admin commands
    def shutdown(self,nick,*args):
        if nick.is_privileged():
            return bot.shutdown()

        return self._unauthorized(nick)

    def promote(self,nick,*args):
        if nick.is_privileged():
            try:
                pnick = args[0]
                NickMemory().promote_nick(pnick)
                return 'Added bot wrangler %s' % pnick

            except IndexError:
                return 'Sorry but I need a name to promote'

        return self._unauthorized(nick)

    def demote(self,nick,*args):
        if nick.is_privileged():
            try:
                pnick = args[0]
                NickMemory().demote_nick(pnick)
                return 'Removed %s as a bot wrangler.' % pnick
            except IndexError:
                return 'Sorry but I need a name to demote.'
        else:
            return self._unauthorized(nick)

    def _unauthorized(self, nick):
        return 'I can\'t let you do that {}'.format(nick)

    # base commands
    def remember(self,nick,*args):
        if len(args) == 2:
            # remembering a history line, usually a silly thing someone said
            srchnick, pattern = args
            nicklines = bot.mem.find_history_by_nick( srchnick, 20 )

            for l in nicklines:
                if pattern in l:
                    bot.mem.remember(srchnick, l[1])

                    return "Ok {}, remembering \"{}\"".format(nick, l[1])
        elif len(args) == 3:
            # remembering a phrase
            bot.mem.remember(args[0], args[2])
            return "Ok {}".format(nick)

    def forget(self,nick,*args):
        command = args[0]
        phrase,resp = command.split(' ')
        if resp:
            bot.mem.forget_response( phrase, resp )
        else:
            bot.mem.forget_all( phrase )

        return "Ok {}".format(nick)

    def whatwasthat(self,nick,*args):
        tonick, response = bot.get_last()   

    def quiet


# uses tuples. Instance will be created then getattr called on the string to execute the method
command_tokens = {}
rules = {}

command_tokens['shutdown'] = (BotCtrl,'shutdown')
command_tokens['promote'] = (BotCtrl,'promote')
command_tokens['demote'] = (BotCtrl,'demote')
command_tokens['remember'] = (BotCtrl,'remember')
command_tokens['forget'] = (BotCtrl,'forget')
command_tokens['whatwasthat'] = (BotCtrl,'whatwasthat')

rules['^shutdown'] = 'shutdown'
rules['^promote ([^\s]+)$'] = 'promote'
rules['^demote ([^\s]+)$'] = 'demote'
rules['^remember ([^\s]+) (.+)$'] = 'remember'
rules['^(.+?) (is) (.+)'] = 'remember'
rules['^forget (.+)$'] = 'forget'
rules['^what.?was.?that\??'] = 'whatwasthat'
