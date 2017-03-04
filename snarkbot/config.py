# where to store the database (maybe a connection string later?)
dbfile = '/tmp/snarkbot.db'

# the minimum time the bot will wait before saying something, even if not
# spoken to
min_wait_seconds = 30

# the max time the bot will wait before saying something.
max_wait_seconds = 120

# the shortest period for snarkbot to be quiet if told in seconds.
# he'll stop talking this long the first time he's told. If he's told again
# we add more up to quiet_max
quiet_period = 60

# see above. Max time snarkbot will be quiet. quiet_modifier time will reset after this
quiet_max = 600

#The number of lines of history to commit to the database
max_history_lines = 1000

# extra paths to look for commands
extra_command_paths = None
