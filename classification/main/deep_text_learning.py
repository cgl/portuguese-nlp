#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,io,traceback,codecs
import gensim
import re
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from pprint import pprint
from gensim.models import word2vec

#BASE_DIR = "/home/graphlab_create/data/blogs" # NOTE: Update BASE_DIR to your own directory path
class TrainSentences(object):
    """
    Iterator class that returns Sentences from texts files in a input directory
    """
    RE_WIHTE_SPACES = re.compile("[\s,]+") # re.compile("\s+")
    STOP_WORDS = set(stopwords.words("portuguese"))
    def __init__(self, dirname):
        """
        Initialize a TrainSentences object with a input directory that contains text files for training
        :param dirname: directory name which contains the text files
        """
        self.dirname = dirname
        #def __iter__(self):
        """
        Sentences iterator that return sentences parsed from files in the input directory.
        Each sentences is returned as list of words
        """
        #First iterate  on all files in the input directory
        for fname in os.listdir(self.dirname):
            # read line from file (Without reading the entire file)
            #for line in io.open(os.path.join(self.dirname, fname), "rb"):
            #for line in file(os.path.join(dirname, fname), "rb"):
            self.get_sentences(fname)

    def get_sentences(self,fname):
        for line in codecs.open(os.path.join(self.dirname, fname),"r",encoding="utf8"):
                # split the read line into sentences using NLTK
                for s in txt2sentences(line, is_html=False):
                    #import ipdb ; ipdb.set_trace()
                    # split the sentence into words using regex
                    w = txt2words(s, lower=False, is_html=False, remove_stop_words=True,
                                                 remove_none_english_chars=False)
                    #skip short sentneces with less than 3 words
                    if len(w) < 3:
                        continue
                    yield w

def txt2sentences(txt, is_html=False, remove_none_english_chars=False):
    """
    Split the English text into sentences using NLTK
    :param txt: input text.
    :param is_html: If True thenremove HTML tags using BeautifulSoup
    :param remove_none_english_chars: if True then remove non-english chars from text
    :return: string in which each line consists of single sentence from the original input text.
    :rtype: str
    """
    #if is_html:
    #    txt = BeautifulSoup(txt).get_text()
    tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    try:
        # split text into sentences using nltk packages
        tokenized = tokenizer.tokenize(txt)
        for s in tokenized:
            #import ipdb ; ipdb.set_trace()
            if remove_none_english_chars:
                #remove none English chars
                s = re.sub("[^a-zA-Z]", " ", s)
            yield s
    except UnicodeDecodeError:
        traceback.print_exc()
        import ipdb ; ipdb.set_trace()

def txt2words(txt, lower=True, is_html=False, remove_none_english_chars=True, remove_stop_words=True):
    """
    Split text into words list
    :param txt: the input text
    :param lower: if to make the  text to lowercase or not.
    :param is_html: If True then  remove HTML tags using BeautifulSoup
    :param remove_none_english_chars: if True then remove non-english chars from text
    :param remove_stop_words: if True then remove stop words from text
    :return: words list create from the input text according to the input parameters.
    :rtype: list
    if is_html:
        txt = BeautifulSoup(txt).get_text()
    if lower:
        txt = txt.lower()
    if remove_none_english_chars:
        txt = re.sub("[^a-zA-Z]", " ", txt)
    """

    words = TrainSentences.RE_WIHTE_SPACES.split(txt.strip().lower())
    if remove_stop_words:
        #remove stop words from text
        words = [w.strip() for w in words if w.strip() not in TrainSentences.STOP_WORDS]
    return words


###################################################

from numpy import average
import graphlab as gl
import numpy as np
import gensim

class DeepTextAnalyzer(object):
    def __init__(self, word2vec_model):
        """
        Construct a DeepTextAnalyzer using the input Word2Vec model
        :param word2vec_model: a trained Word2Vec model
        """
        self._model = word2vec_model

    def txt2vectors(self,txt, is_html):
        """
        Convert input text into an iterator that returns the corresponding vector representation of each
        word in the text, if it exists in the Word2Vec model
        :param txt: input text
        :param is_html: if True, then extract the text from the input HTML
        :return: iterator of vectors created from the words in the text using the Word2Vec model.
        """
        words = txt2words(txt,is_html=is_html, lower=False, remove_none_english_chars=False)
        words = [w for w in words if w in self._model]
        if len(words) != 0:
            for w in words:
                yield self._model[w]


    def txt2avg_vector(self, txt, is_html):
        """
        Calculate the average vector representation of the input text
        :param txt: input text
        :param is_html: is the text is a HTML
        :return the average vector of the vector representations of the words in the text
        """
        vectors = self.txt2vectors(txt,is_html=is_html)
        vectors_sum = next(vectors, None)
        if vectors_sum is None:
            return None
        count =1.0
        for v in vectors:
            count += 1
            vectors_sum = np.add(vectors_sum,v)

        #calculate the average vector and replace +infy and -inf with numeric values
        avg_vector = np.nan_to_num(vectors_sum/count)
        return avg_vector

"""
for line in codecs.open("classification/data/v4/test2/d0196.txt","r",encoding="utf8"):
    for s in txt2sentences(line, is_html=False):
        w = txt2words(s, lower=False, is_html=False, remove_stop_words=True,
                      remove_none_english_chars=False)

for sen in sentences:
    try:
        sentence= [s.encode('latin1') for s in sen]
    except UnicodeEncodeError:
        sentence = [s.replace(u'\u2013',u'\xe3').encode('latin1') for s in sen]
    print("%s %s" %(i," ".join(sentence)))
"""

def add_arguments(sframe,folder,label,vec_model):
    data = {'filenames':[], 'text': [] } #, 'vectors': [], 'boW': [], 'rel': []}
    for fname in os.listdir(folder):
        data['filenames'].append(fname)
        with codecs.open(os.path.join(folder, fname),"r",encoding="utf8") as infile:
            data['text'].append(infile.read())
    sf = gl.SFrame(data)
    dt = DeepTextAnalyzer(vec_model)
    sf['vectors'] = sf['text'].apply(lambda p: dt.txt2avg_vector(p, is_html=False))
    size = len(data['filenames'])
    if label is not None:
        sf['rel'] = [label]*size
    sf['1gram features'] = gl.text_analytics.count_ngrams(sf['text'], 1)
    sf['2gram features'] = gl.text_analytics.count_ngrams(sf['text'], 2)
    return sframe.append(sf1)



def train_classifier(sf):
    """
    train_set = sf
    train_set, test_set = sf.random_split(0.8, seed=5)
    clsv = gl.classifier.create(train_set, target="rel",features=['vectors'])
    cls = gl.classifier.create(train_set, target="rel",features=['1gram features'])
    cls1 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features'])
    cls2 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features','2gram features'])

    linear_model = gl.linear_regression.create(train_set, target='rel',features=['vectors'])
    linear_model.evaluate(test_set)


    for mdl in [clsv,cls,cls1,cls2]:
        mdl.evaluate(test_set)
    """

    cls1 = gl.classifier.create(sf, target="rel",features=['vectors','1gram features'])
    return cls1

def test_classifier(vec_model):

    cls1 = train_classifier(vec_model)
    test_folder = "/tmp/temp/"
    dataset = add_arguments(test_folder,None,vec_model)
    result171_dataset = cls1.classify(dataset)

    triggers = add_trigger_feature()

    count = 0 ; positives=0 ; shape= 100 # dataset.shape[0]
    for ind in range(0,shape):
            if result171_dataset["class"][ind]:
                    positives+=1
                    if check_trigger_exist(dataset['1gram features'][ind]):
                            count+=1
                            print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

    for ind in range(0,10): #dataset.shape[0]
        if result171_dataset["class"][ind]:
            positives+=1
            if check_trigger_exist(dataset['1gram features'][ind]):
                count+=1
                print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

    for ind in range(0,dataset.num_rows()):
        if result_dataset['class'][ind]:
            print("http://mann.cmpe.boun.edu.tr/folha_data/%s %s" %(dataset['filenames'][ind].replace("_","/"),result_dataset['probability'][ind]))

def check_trigger_exist(grams):
    flag=False
    for token in grams.keys():
        if token.strip().decode('latin1') in triggers:
            print(token)
            flag=True
    return flag

def add_trigger_feature():
    filename = "classification/data/trigger_tokens.txt"
    with codecs.open(filename, "r", encoding="utf8") as infile:
        trigger_str = infile.read()
    triggers = list(set(trigger_str.split(",")))
    return triggers

def main():
    vec_model = word2vec.Word2Vec.load_word2vec_format('/tmp/model.txt',binary=False)
    irr_folder="classification/data/v4/class_irr/" ; folder=irr_folder
    rel_folder="classification/data/v4/test2/" ; folder=rel_folder
    sf = gl.SFrame()
    sf = add_arguments(sf,rel_folder,1,vec_model)
    sf = add_arguments(irr_folder,0,vec_model)
