import re
from math import log
from string import ascii_lowercase
from heapq import nlargest
import marshal
from pprint import pprint

py_freq= {}
p2c = {}
py_short = {}
MAX_SEARCH_ENTRIES = 1000
MAX_SHOW_ENTRIES = 15

py_freq = marshal.load(file('data/py.freq','rb'))
p2c = marshal.load(file('data/p2c.map','rb'))
chn_freq = marshal.load(file('data/chn.freq','rb'))

min_freq = min(py_freq.values())
single_letters = set(ascii_lowercase)

print "data loaded."

def word_rank(word):
    if word in single_letters:
        return min_freq-1.0
    elif len(word)==1:
        return 0.0
    return py_freq.get(word,min_freq*20.0)

def dp_cut(sentence,topK=3):
     max_word_len=20
     path = {}
     N = len(sentence)
     path[N] = [ [] ]
     for i in xrange(N-1,-1,-1):
          path[i] = []
          for hop in xrange(i+1,min(i+max_word_len+1,N+1)):
            if (sentence[i:hop] in py_freq)  or (hop-i==1):
                for pt in path[hop]:
                    path[i].append([sentence[i:hop]] + pt)
            path[i] = sorted(path[i],key=lambda L:sum(word_rank(x) for x in L), reverse=True)[:topK]
     return path[0]

def all_combine_idx(m,idx,tb):
    if idx==len(m)-1:
        for i in xrange(0,len(m[idx])):
            if tb['n']>MAX_SEARCH_ENTRIES:
                return
            yield [i]
            tb['n']=tb.get('n',0)+1  
    else:
        for w in xrange(0,len(m[idx])):
            if tb['n']>MAX_SEARCH_ENTRIES:
                    return
            for sub in all_combine_idx(m,idx+1,tb):
                if tb['n']>MAX_SEARCH_ENTRIES:
                    return
                yield [w]+sub

def chn_rank(word):
    q = chn_freq.get(word,min_freq*20)
    return q

def all_combine(m,idx):
    tb = {'n':0}
    all_index_list = sorted(all_combine_idx(m,idx,tb),key=lambda L: sum(chn_rank(m[i][j]) for i,j in enumerate(L) ) ,reverse=True)
    if len(m)>1:
        all_index_list = all_index_list[:MAX_SHOW_ENTRIES]
    for column in all_index_list:
        yield "\n".join(m[i][column[i]] for i in xrange(len(m)))

def guess_words_no_sort(sentence):
    if len(sentence)>0:
        bucket = {}
        showed = 0
        for py_list in dp_cut(sentence):
            sub_showed = 0
            if showed>=MAX_SHOW_ENTRIES:
                break
            m=[]
            for p in py_list:
                if len(p)<6:
                    if len(py_list)==1: #single character, show all candidates
                        span = MAX_SEARCH_ENTRIES
                    else:
                        span = 6
                else:
                    span = 3
                m.append( p2c.get(p,[p])[:span] )
            
            for c in all_combine(m,0):
                if sub_showed>=MAX_SHOW_ENTRIES/2:
                    break
                if not c in bucket:
                    yield c
                    bucket[c]=1
                    if len(c)>1:
                        showed+=1
                        sub_showed+=1
                    if sub_showed>=MAX_SHOW_ENTRIES/2:
                        break
        del bucket

def guess_words(sentence):
    result = guess_words_no_sort(sentence)
    st_list = sorted( [(sum(chn_rank(word) for word in s.split('\n')),s) for s in result], reverse=True)
    return [x[1].replace("\n",'') for x in st_list]

if __name__ == "__main__":
    while True:
        py_sentence = raw_input("")
        gussed_words = guess_words(py_sentence)
        print ",  ".join(gussed_words )

