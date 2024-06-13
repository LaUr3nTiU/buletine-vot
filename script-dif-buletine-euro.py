import json
import sys
import lib

modes = ['P', 'CL', 'CJ', 'PCJ']

fname = 'db/euro/pv_%s_part.json'
STAGE = 'PART'
base_link = 'https://prezenta.roaep.ro/locale09062024/'

judete = lib.eurojudete

for judet in judete:
  f = open((fname % judet))
  data = json.load(f)

  entries = data['stages'][STAGE]['scopes']['PRCNCT']['categories']['EUP']['table']

  for table_id in entries:
    precinct = entries[table_id]
    for nr in precinct['fields']:
      if nr['name'] == 'b':
        b = int(nr['value'])
      if nr['name'] == 'c':
        c = int(nr['value'])
      if nr['name'] == 'd':
        d = int(nr['value'])
      if nr['name'] == 'e':
        e = int(nr['value'])
      if nr['name'] == 'f':
        f = int(nr['value'])

    expected = d+e+f
    dif = c - expected
    pno = int(precinct['precinct_nr'])
    if dif != 0:
      files = data['stages'][STAGE]['scopes']['PRCNCT']['categories']['EUP']['files']
      flink = 'missing'
      version = 0
      for fno in files:
        if fno == precinct['precinct_id']:
          for fdata in files[fno]:
            if fdata['type'] == 'GNRTD':
              fv = int(fdata['version'])
              if fv > version:
                version = fv
                flink = base_link + fdata['url']

      fmt = ('%d, %d, %d, %d, %d, %d, %s, %s, %s' % (dif, b, c, d, e, f, precinct['county_code'], precinct['precinct_nr'], flink))
      print(fmt)
      #sys.exit(0)

  #sys.exit(0)
