import json
import sys

judet = 'gl'

f = open(('db/pv_%s_part.json' % judet))
data = json.load(f)

mode = 'CL' # can be P, CJ, PJ

entries = data['stages']['PART']['scopes']['PRCNCT']['categories'][mode]['table']
fmt = json.dumps(data, indent=1)
print(fmt)
