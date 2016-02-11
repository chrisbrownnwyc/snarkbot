# loads in positive and negative words
import sys
sys.path.append('..')
import os
import argparse
from snarkbot import config

config.dbfile = '../snarkbot.db'
from snarkbot import db

parser = argparse.ArgumentParser(description="Import positive and negative words to create a sentiment database for snarkbot")
parser.add_argument('--negative','-n',metavar='FILE', help="A file of negative words", dest='negative')
parser.add_argument('--positive','-p',metavar='FILE', help="A file of positive words", dest='positive')

args = parser.parse_args()

if not db.has_table('sentiment'):
	db.session.execute("CREATE TABLE sentiment (word text, score integer)")

sql = "INSERT INTO sentiment VALUES(?,?)"
if os.path.exists(args.negative):
	print "Loading negative words"
	nfh = open(args.negative,"rb")
	ncount = 0
	nlines = nfh.readlines()
	for line in nlines:
		if line.startswith(' ') or line.startswith(';'):
			continue
		
		ncount += 1
		db.session.execute(sql, [unicode(line.strip().decode('utf-8','ignore')), -1])

	nfh.close()

	print "Loaded %d negative words." % ncount

if os.path.exists(args.positive):
	print "Loading positive values"
	pfh = open(args.positive,"r")
	pcount = 0
	lines = pfh.readlines()
	for line in lines:

		if line.startswith(' ') or line.startswith(';'):
			continue
		pcount += 1
		db.session.execute(sql,[unicode(line.strip().decode('utf-8','ignore')),-1])
	pfh.close()
	print "Loaded %d positive words" % pcount

db.conn.commit()
print "Done"
