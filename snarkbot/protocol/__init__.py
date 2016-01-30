import os
# hackish way to load all the retrievers dynamically
importpath = os.path.dirname(os.path.abspath(__file__))
for f in os.listdir(importpath):
	if os.path.isfile( os.path.join(importpath,f) ) and f.endswith('.py'):
		node = __import__( f[:-3], globals(), locals() )
		for k in dir(node):
			if 'Protocol' in k:
				locals()[k] = getattr(node, k)
