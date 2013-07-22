import re
from math import log
from string import ascii_lowercase
from heapq import nlargest
import marshal

py_freq= {}
p2c = {}
py_short = {}
re_eng = re.compile('([a-zA-Z]+)')
MAX_FREQ = 260000
MAX_SEARCH_ENTRIES = 1000
MAX_SHOW_ENTRIES = 15

for line in open("freq.txt"):
    line = line.rstrip()
    py,freq = line.split(' ')
    freq = float(freq)
    if freq>MAX_FREQ: #cut the over-high frequency
        freq = MAX_FREQ
    py_freq[py] = py_freq.get(py,0)+freq

for line in open("p2c.txt"):
    line = line.decode('utf-8').rstrip()
    py,words = line.split(' ')
    p2c[py] = words.split(',')


for line in open("short.txt"):
    line = line.decode('utf-8').rstrip()
    py,words = line.split(' ')
    py_short[py] = words.split(',')

total = sum(py_freq.values())
py_freq = dict( (k,log(v/total)) for k,v in py_freq.iteritems())

marshal.dump(py_freq,open("data/py.freq",'wb'))
marshal.dump(p2c,open("data/p2c.map",'wb'))
marshal.dump(py_short,open("data/short.map",'wb'))
