import requests
import sys
import lib

headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
'Accept-Encoding': 'gzip, deflate, br, zstd',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

payload = {}

for judet in lib.eurojudete:
    fname = ('db/euro/pv_%s_part.json' % judet)
    ts = 1718308827917
    link = ('https://prezenta.roaep.ro/europarlamentare09062024/data/json/sicpv/pv/pv_%s_part.json?_=%d' % (judet, ts))

    response = requests.get(link, headers=headers)
    f = open(fname, 'w')
    f.write(response.text)
    f.close()
    print("Written %s" % judet)
