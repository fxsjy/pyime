import re
from math import log
from string import ascii_lowercase
from heapq import nlargest

py_freq= {}
p2c = {}
py_short = {}
re_eng = re.compile('([a-zA-Z]+)')

for line in open("freq.txt"):
    line = line.rstrip()
    py,freq = line.split(' ')
    py_freq[py] = py_freq.get(py,0)+float(freq)

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

min_freq = min(py_freq.values())
single_letters = set(ascii_lowercase)
print "data loaded."

def word_rank(word):
    if word in single_letters:
        return min_freq-1.0
    elif len(word)==1:
        return 0.0
    return py_freq.get(word,min_freq*20.0)

def dp_cut(sentence):
     max_word_len=20
     best_hop = {}
     N = len(sentence)
     best_hop[N] = [(0,N)]
     for i in xrange(N-1,-1,-1):
          best_hop[i] = nlargest(2,[ (word_rank(sentence[i:hop]) + best_hop[hop][0][0],hop) for hop in xrange(i+1,min(i+max_word_len+1,N+1)) ])
     start  = 0
     top1 = []
     while start<N:
          top1.append(sentence[start:best_hop[start][0][1]])
          start = best_hop[start][0][1]
     top2 = []
     start = 0
     while start<N:
        if start==0 and len(best_hop[start])>1:
            top2.append(sentence[start:best_hop[start][1][1]])
            start = best_hop[start][1][1]
        else:
            top2.append(sentence[start:best_hop[start][0][1]])
            start = best_hop[start][0][1]
     return [top1,top2]

def all_combine(m,idx,ct):
    if idx==len(m)-1:
        for w in m[idx]:
            yield w
    else:
        for w in m[idx]:
            i=0
            for sub in all_combine(m,idx+1,ct):
                yield w+sub
                i+=1
                if i>=ct:
                    break

def pyshort_filter(mixed,ct):
    mixed = mixed.replace("'","")
    m = []
    for chunk in re_eng.split(mixed):
        if not (chunk in py_short):
            m.append([chunk])
        else:
            m.append(py_short[chunk][:ct])
    for c in all_combine(m,0,ct):
        yield c

def guess_words(sentence,ct=3):
    if len(sentence)>0:
        for py_list in dp_cut(sentence):
            m=[]
            if len(py_list)==1:
                ct = 30
            else:
                ct = 3
            for p in py_list:
                m.append( p2c.get(p,[p])[:ct] )
            for c in all_combine(m,0,ct):
                for cc in pyshort_filter(c, ct):
                    yield cc

if __name__ == "__main__":
    while True:
        py_sentence = raw_input("")
        print ",  ".join( guess_words(py_sentence))

