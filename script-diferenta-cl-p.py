import json
import sys
import lib

modes = ['P', 'CL', 'CJ']

fname = 'db/locale/pv_%s_part.json'
STAGE = 'PART'
base_link = 'https://prezenta.roaep.ro/locale09062024/'

#judete = lib.judete

off_l =  25 # minimum allowed difference
off_h = 175 # maximum allowed difference
city = 'bv' # can be s2 or bv

if city == 's1':
  judete = ['b']
  pno_b = 1
  pno_e = 166
elif city == 's2':
  judete = ['b']
  pno_b = 167
  pno_e = 368
elif city == 'bv':
  judete = ['bv']
  pno_b = 1
  pno_e = 188

ADU = 'ALIANȚA DREAPTA UNITĂ USR - PMP - FORȚA DREPTEI'
UPB = 'ALIANȚA UNIȚI PENTRU BRAȘOV'
PSDNL = 'ALIANȚA ELECTORALĂ PSD PNL'
PSD = 'PARTIDUL SOCIAL DEMOCRAT'
PNL = 'PARTIDUL NAȚIONAL LIBERAL'

results = {}
for x in range(1, 2000):
  results[x] = {'judet': '', 'sectia': 0, 'votes_P': {}, 'votes_CL': {}}

for judet in judete:
  f = open((fname % judet))
  data = json.load(f)

  for mode in modes:
    entries = data['stages'][STAGE]['scopes']['PRCNCT']['categories'][mode]['table']

    for table_id in entries:
      precinct = entries[table_id]
      usr = 0
      psd = 0
      for vote in precinct['votes']:
        party = vote['party']
        cnddt = vote['candidate']
        count = int(vote['votes'])
        if mode == 'P':
          if party == ADU or party == UPB:
            usr = count
          elif party == PSDNL:
            psd = count
        elif mode == 'CL':
          if cnddt == ADU or cnddt == UPB:
            usr = count
          elif cnddt == PSDNL:
            psd = count
        elif mode == 'CJ':
          if cnddt == ADU:
            usr = count
          elif cnddt == PNL or cnddt == PSD:
            psd += count

      pno = int(precinct['precinct_nr'])
      #results[pno].append({'mode': mode, 'judet': precinct['county_code'], : {'usr': usr, 'psd': psd}})
      results[pno][('votes_%s' % mode)] = {'usr': usr, 'psd': psd}
      results[pno]['judet'] = precinct['county_code']
      results[pno]['sectia'] = pno
      #fmt = ('%d, %d, %s, %s, %s' % (usr, psd, precinct['county_code'], precinct['precinct_nr'], mode))
      #print(fmt)

    #sys.exit(0)
  #sys.exit(0)

for pno in results:
  if pno >= pno_b and pno <= pno_e:
    # sectia 56 nu este uploadata (in s1)
    if 'usr' in results[pno]['votes_P']:
      p_usr = results[pno]['votes_P']['usr']
      p_psd = results[pno]['votes_P']['psd']
      cl_usr = results[pno]['votes_CL']['usr']
      cl_psd = results[pno]['votes_CL']['psd']
      if cl_usr > 0 and cl_psd > 0:
        pc_usr = round(p_usr / cl_usr * 100, 2)
        pc_psd = round(p_psd / cl_psd * 100, 2)
        if pc_usr < off_l or pc_usr > off_h or pc_psd < off_l or pc_psd > off_h:
          print("sectia[%d] ratio (P/CL): USR[%d/%d = %d%%] PSD[%d/%d = %d%%]" % (pno, p_usr, cl_usr, pc_usr, p_psd, cl_psd, pc_psd))
      else:
        print("Zero pe CL: USR[%d/%d] PSD[%d/%d]" % (p_usr, cl_usr, p_psd, cl_psd))
