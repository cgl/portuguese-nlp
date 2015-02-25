import nltk,random
tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
from nltk.tokenize import word_tokenize
import crawler

def words_in_doc(content):
    sentences = tokenizer.tokenize(content.text)
    for sent in sentences:
        words = word_tokenize(sent)
        return words

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

"""
pages_pos = [] ; crawler.crawl("data/relevant.txt",pages_pos)
pages_neg = [] ; crawler.crawl("data/irrelevant.txt",pages_neg)
training_pos = [] ; test_pos = [] ; crawler.parse_pages(pages_pos, training_pos,test_pos, 'pos')
training_neg = [] ; test_neg = [] ; crawler.parse_pages(pages_neg, training_neg,test_neg, 'neg')

training_documents = [(words_in_doc(doc[0]),doc[1]) for docs in [training_pos[0:170],training_neg[0:172]] for doc in docs]

documents = [(words_in_doc(doc[0]),doc[1]) for docs in [training_pos[0:170],training_neg[0:172],test_pos[0:342],test_neg[0:344]] for doc in docs]

word_lists = [words_in_doc(doc[0])
              for docs in [training_pos[0:170],training_neg[0:172],test_pos[0:342],test_neg[0:344]]
              for doc in docs]
all_words = nltk.FreqDist(w.lower() for word_list in word_lists if word_list for w in word_list)
word_features = all_words.keys()[:2000]

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
"""
