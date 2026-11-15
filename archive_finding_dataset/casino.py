from convokit import Corpus, download
import json

# corpus = Corpus(filename=download("casino-corpus"))

data = []
with open('./casino_corpus/utterances.jsonl') as f:
    for line in f:
        data.append(json.loads(line))
data1 = []
for item in data:
    if item["conversation_id"]=='utterance_0':
        data1.append(item)
for item in data1:
    print(item['text'])
    print('\n')