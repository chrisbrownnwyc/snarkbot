import re
import signal

# talk on the command line
# note this is *nix only due to the use of signal

class PromptTimeoutError(Exception):
    pass

def handle_prompt_timeout(signum,frame):
    raise PromptTimeoutError

class CmdProtocol(object):
    def __init__(self):
        self.send('What\'s your name?',None)
        self.capture_name = True
        self.with_nick = None
    
    def send(self,msg,nick=None):
        # nick doesn't really matter since its always one person
        print msg

    def read(self,timeout=30):

        signal.signal(signal.SIGALRM, handle_prompt_timeout )
        signal.alarm(timeout)
        try:
            _response = raw_input("> ")
            # check if the respondant is setting their name
            is_name_response = self._check_nick(_response)
            if is_name_response:
                return False
            
            return (self.with_nick, response.strip())

        except PromptTimeoutError:
            # no one said anything
            return False


    def _check_nick(self, response):
        
        matches = re.search('(call me|my name is)\s+([^\s]+)')
        if matches:
            self.capture_name = True
        
        if self.capture_name:
            if matches:
                try:
                    response = response.replace(matches.group(1))
                except:
                    pass

            self.with_nick = response.strip()
            self.send("Ok, I'll call you %s" % self.with_nick)
            self.capture_name = False
            return True

        return False

    def close(self):
        # nothing needed here
        pass
