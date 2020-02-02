import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


with open(sys.argv[0],'r')  as  f:
    text=" ".join(f.readlines())
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(text)
for word in [w for w in word_tokens if len(w)>3 and not w in stop_words]:
    word=word.strip(' \n,.=!_\'')
    word.replace(".","_")
    print(word)
