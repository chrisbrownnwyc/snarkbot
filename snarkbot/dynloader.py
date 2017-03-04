from __future__ import absolute_import
import os
import sys

# hackish way to load things from a directory
def loader(importpath,cls):
    loadvars = {}
    sys.path.append(importpath)
    for f in os.listdir(importpath):
        if os.path.isfile( os.path.join(importpath,f) ) and f.endswith('.py'):
            node = __import__( f[:-3], globals(), locals() )
            for k in dir(node):
                if issubclass(k,cls):
                    loadvars[k] = getattr(node, k)

    return loadvars
