import json
import sys
import lib

modes = ['P', 'CL', 'CJ']

fname = 'db/pv_%s_part.json'
STAGE = 'PART'
base_link = 'https://prezenta.roaep.ro/locale09062024/'

#judete = lib.judete
judete = ['b']

ADU = 'ALIANȚA DREAPTA UNITĂ USR - PMP - FORȚA DREPTEI'
PSDNL = 'ALIANȚA ELECTORALĂ PSD PNL'
PSD = 'PARTIDUL SOCIAL DEMOCRAT'
PNL = 'PARTIDUL NAȚIONAL LIBERAL'

results = {}
for x in range(1, 1290):
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
        count = int(vote['votes'])
        if mode == 'P':
          if vote['party'] == ADU:
            usr = count
          elif vote['party'] == PSDNL:
            psd = count
        elif mode == 'CL':
          if vote['candidate'] == ADU:
            usr = count
          elif vote['candidate'] == PSDNL:
            psd = count
        elif mode == 'CJ':
          if vote['candidate'] == ADU:
            usr = count
          elif vote['candidate'] == PNL or vote['candidate'] == PSD:
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

# sector_1:   1 -> 166
# sector_2: 167 -> 368
for pno in results:
  #if pno >= 1 and pno <= 166:
  if pno >= 167 and pno <= 368:
    # sectia 56 nu este uploadata
    if 'usr' in results[pno]['votes_P']:
      p_usr = results[pno]['votes_P']['usr']
      p_psd = results[pno]['votes_P']['psd']
      cl_usr = results[pno]['votes_CL']['usr']
      cl_psd = results[pno]['votes_CL']['psd']
      if cl_usr > 0 and cl_psd > 0:
        pc_usr = round(p_usr / cl_usr * 100, 2)
        pc_psd = round(p_psd / cl_psd * 100, 2)
        if pc_usr < 50 or pc_usr > 150 or pc_psd < 50 or pc_psd > 150:
          print("sectia[%d] ratio (P/CL): USR[%d/%d = %d%%] PSD[%d/%d = %d%%]" % (pno, p_usr, cl_usr, pc_usr, p_psd, cl_psd, pc_psd))
      else:
        print("Zero pe CL: USR[%d/%d] PSD[%d/%d]" % (p_usr, cl_usr, p_psd, cl_psd))
