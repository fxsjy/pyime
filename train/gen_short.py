import xpinyin
P = xpinyin.Pinyin()

d={}
for line in open('dict.txt'):
    line = line.decode('utf-8').strip()
    word,freq,_ = line.split(' ')
    py = P.get_pinyin(word)
    tmp = py.split('-')
    short = "".join([a[0] for a in tmp])
    d[short] = d.get(short,[])+[(int(freq),word)]

for k,v in d.iteritems():
    print k,",".join(v[1] for v in sorted(v,reverse=True) )
