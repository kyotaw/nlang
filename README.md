nlang
====

natural language processing library for Janpanese.  
This includes the following processors:  
* Tokenizer - Tokenizer is a morphological analyser. This divides raw string stream into morphemes and assigns parts of speech to each of them.
* Chunker - Chunker genarates phrases from morphemes.
* Sentencer - Sentencer divides raw string stream into sentences based on appropriate delimiters. This also have learning feature to learn delimiters used in text.
* Clusterizer - Clusterizer generates some groups of documents which are similar to each oher.

## Requirement
Python 3.4.2 or later

## Usage
* Tokenizer  
```python
from nlang.processor.tokenizer import Tokenizer

tokenizer = Tokenizer()
words = tokenizer.tag('世界の半分をお前にあげる')

for word in words:
    print(word)

==> 世界,セカイ,世界,名詞,一般,,
==> の,ノ,の,助詞,連体化,,
==> 半分,ハンブン,半分,名詞,副詞可能,,
==> を,ヲ,を,助詞,格助詞,一般,,
==> お前,オマエ,お前,名詞,代名詞,一般,,
==> に,ニ,に,助詞,格助詞,一般,,
==> あげる,アゲル,あげる,動詞,自立,一段,基本形
```

* Chunker  
```python
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.chunker import Chunker

tokenizer = Tokenizer()
words = tokenizer.tag('世界の半分をお前にあげる')

chunker = Chunker()
chunks = chunker.clause(words)

for chunk in chunks:
    lemmas = [w.lemma for w in chunk]
    print(lemmas)

==> ['世界', 'の']
==> ['半分', 'を']
==> ['お前', 'に']
==> ['あげる']
```

* Sentencer  
```python
from nlang.processor.sentencer import Sentencer

sentencer = Sentencer(False)
sents = sentencer.sentences('おはようございます。では、さようなら')

for sent in sents:
    print(sent)
    
==> おはようございます。
==> では、さようなら
```

* Clusterizer  
```python
from nlang.processor.tokenizer import Tokenizer
from nlang.processor.clusterizer.clusterizer import Clusterizer

tokenizer = Tokenizer()
clusterizer = Clusterizer()

f_1 = open('weather_1')
doc_1 = tokenizer.tag(f_1.read())
clusterizer.add_document(doc_1, 'weather_1')
f_2 = open('traffic_1')         
doc_2 = tokenizer.tag(f_2.read())
clusterizer.add_document(doc_2, 'traffic_1')
f_3 = open('weather_2')         
doc_3 = tokenizer.tag(f_3.read())
clusterizer.add_document(doc_3, 'weather_2')
f_4 = open('traffic_2')
doc_4 = tokenizer.tag(f_4.read())
clusterizer.add_document(doc_4, 'traffic_2')
 
clusters = clusterizer.clusterize(cluster_num=2)

print(clusters[0])      
==> ['weather_1', 'weather_2']
print(clusters[1])
==> ['traffic_1', 'traffic_2']
```
