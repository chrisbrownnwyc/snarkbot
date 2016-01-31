import os
from dynloader import loader

importpath = os.path.dirname(os.path.abspath(__file__))
localvars = loader(importpath,'Protocol')
locals().update(**localvars) # ok that's kind of cool
