#USE COMMAND "python3 gauravmi.py train.labeled test.unlabeled 5 0.2"

import sys

def ngrams(inpu, n):
  
  inpu=inpu.strip()
  inpu="#"*(n-1) + inpu + "#"*(n-1)
  output = []
  for i in range(len(inpu)-n+1):
    output.append(inpu[i:i+n])
  return output


def prob_ngrams(ng,c,lamb,lang_probs,lang_ngrams,counter) :
  pc=lang_probs[c]
  
  
 
  words_for_lang=len(lang_ngrams[c])
  

  for n in ng:
    if n in lang_ngrams[c]:
      nv=lang_ngrams[c][n]

    else:
      nv=0
    
    
    
    
    pc=pc*(nv +lamb )/( ( words_for_lang +lamb*counter)/100000)
  return pc
 

def find_language(grams,lamb):
  lang=[]
  lang_probs=dict()
  languages=['eng', 'hun', 'fre', 'vie', 'swe', 'cze', 'spa', 'ita', 'fin', 'dan', 'slo', 'pol', 'ind', 'ice', 'nor', 'ger', 'por', 'tur', 'rum', 'ell', 'dut'] 
  lang_ngrams=dict()
  ans=""
  num_docs=0
  with open (sys.argv[1]  ,encoding="utf8") as f:
      for langu in languages:
        lang_ngrams[langu] ={} 
      for line in f:
          num_docs+=1
          line=line.strip('\n')
          l=line.split('|')
          lang.append(l[2])
          
          d=l[1]
          la=l[2]
          dn= ngrams(d,grams)
          
          for ngl in dn:
            if  ngl not in lang_ngrams[la]:
              lang_ngrams[la][ngl]=1

            else:
              lang_ngrams[la][ngl]+=1

  
  f.close()
  for s in languages:
    lang_probs[s]=lang.count(s)/num_docs
    
  
  dictlist=[]
  
  for c in languages:
    for key,value in lang_ngrams[c].items():
      dictlist.append(key)
          
  counter=len(set(dictlist))
       
  accu=0
  numlines=0
  with open (sys.argv[2]  ,encoding="utf8") as f2:
    
      for line1 in f2:
          numlines+=1
          line1=line1.strip('\n')
          l=line1.split('|')
          docid=l[0]
          ddev=l[1]
          
          each_lang=[]
          
          findgrams=ngrams(ddev ,grams)
          for ln in languages:
    
              each_lang.append(prob_ngrams(findgrams,ln,lamb,lang_probs,lang_ngrams,counter))  
          
          ans+= docid + "|" + languages[each_lang.index(max(each_lang))] +"\n"
          
          
  f2.close()
  sys.stdout.write(ans)

find_language(int(sys.argv[3]),float(sys.argv[4]))



