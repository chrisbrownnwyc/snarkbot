import os

# hackish way to load things from a directory
def loader(importpath,classname):
	loadvars = {}
	for f in os.listdir(importpath):
		if os.path.isfile( os.path.join(importpath,f) ) and f.endswith('.py'):
			node = __import__( f[:-3], globals(), locals() )
			for k in dir(node):
				if classname in k:
					loadvars[k] = getattr(node, k)

	return loadvars
