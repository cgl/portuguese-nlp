import nltk
tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
from nltk.tokenize import word_tokenize

def words_in_doc(content):
    sentences = tokenizer.tokenize(content.text)
    for sent in sentences:
        words = word_tokenize(sent)
        return words
