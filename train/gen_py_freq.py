import xpinyin
P = xpinyin.Pinyin()

d={}
for line in open('dict.txt'):
	line = line.decode('utf-8').strip()
	word,freq,_ = line.split(' ')
	py = P.get_pinyin(word,'')
	d[py] = d.get(py,0)+int(freq)

for k,v in d.iteritems():
	print k,v
