import nltk,random
tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
from nltk.tokenize import word_tokenize
import crawler
from nltk.corpus import stopwords
#STOPWORDS = stopwords.words('portuguese')

def words_in_doc(content):
    sentences = tokenizer.tokenize(content.text)
    for sent in sentences:
        words = word_tokenize(sent)
        return words #[word for word in words if word not in STOPWORDS]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def get_pages():
    pages_pos = [] ; crawler.crawl("data/relevant.txt",pages_pos)
    pages_neg = [] ; crawler.crawl("data/irrelevant.txt",pages_neg)

    import pickle
    with open("data/pages_neg.pickle","wb") as n_out , open("data/pages_pos.pickle","wb") as p_out:
        pickle.dump(pages_neg,n_out)
        pickle.dump(pages_pos,p_out)

def train(pages_pos,pages_neg):
    training = [] ; test = [] ; crawler.parse_pages(pages_pos, training,test, 'pos')
    crawler.parse_pages(pages_neg, training,test, 'neg')

    documents = [(words_in_doc(doc[0]),doc[1])
                 for docs in [training,test]
                 for doc in docs if doc]

    word_lists = [words_in_doc(doc[0])
                  for docs in [training,test]
                  for doc in docs if doc]
    all_words = nltk.FreqDist(w.lower() for word_list in word_lists if word_list for w in word_list)
    word_features = all_words.keys()[:2000]

    featuresets = [(document_features(d), c) for (d,c) in documents if d]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier
