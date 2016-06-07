#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TrainSentences import txt2words

import os,io,traceback,codecs
import re,nltk
from numpy import average
import graphlab as gl
import numpy as np
from gensim.models import word2vec

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
    if sframe is None:
        sframe = gl.SFrame()
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
    return sframe.append(sf)



def train_classifier(sf):
    cls1 = gl.classifier.create(sf, target="rel",features=['vectors','1gram features'])
    return cls1

def test_classifier(cls1,vec_model):
    test_folder = "/home/cagil/brazil/all_files_parsed/" # "/tmp/temp/"
    dataset = add_arguments(None,test_folder,None,vec_model)
    result171_dataset = cls1.classify(dataset)
    return dataset,result171_dataset

def print_url(dataset,result171_dataset,ind):
    print("http://mann.cmpe.boun.edu.tr/folha_data/%s %s" %(dataset['filenames'][ind].replace("_","/"),result171_dataset['probability'][ind]))

def print_positives_and_confidence(dataset,result171_dataset):
    for ind in range(0,result171_dataset.num_rows()):
        if result171_dataset['class'][ind]:
            print_url(dataset,result171_dataset,ind)

def count_positives_with_trigger(dataset,result171_dataset):
    triggers = add_trigger_feature()
    count = 0 ; positives=0
    for ind in range(0,result171_dataset.num_rows()):
        if result171_dataset["class"][ind]:
            positives+=1
            if check_trigger_exist(dataset['1gram features'][ind]):
                count+=1
                print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

def count_positives_with_mortes(result171_dataset): # dataset.shape[0]
    count = 0 ; positives=0
    for ind in range(0,dataset.num_rows()):
        if result171_dataset["class"][ind]:
            positives+=1
            if "mortes" in dataset['1gram features'][ind].keys():
                count+=1
                print("[%s] %s" %(ind,result171_dataset["probability"][ind]))
    print("%s/%s" %(count,positives))

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

def add_dev(sf,vec_model):
    dev_irr = "classification/data/v4_dev/class_irr/"
    dev_rel ="classification/data/v4_dev/class_rel/"
    sf = add_arguments(sf,dev_irr,0,vec_model)
    sf = add_arguments(sf,dev_rel,1,vec_model)
    return sf

def performance(sf):
    train_set, test_set = sf.random_split(0.8, seed=5)
    cls1 = gl.classifier.create(train_set, target="rel",features=['vectors','1gram features'])
    results = cls1.evaluate(test_set)
    print(results)
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


def main():
    vec_model = word2vec.Word2Vec.load_word2vec_format('word2vec_model.txt',binary=False)
    irr_folder="classification/data/v5/class_irr/"
    rel_folder="classification/data/v5/class_rel/"
    sf = add_arguments(None,rel_folder,1,vec_model)
    sf = add_arguments(sf,irr_folder,0,vec_model)

    cls1 = train_classifier(sf)
    #test_classifier(cls1,vec_model)

    df = add_dev(sf,vec_model)
    cls2 = train_classifier(df)
    cls2.save("my_classifier_file.txt")
    #dataset,result171_dataset = test_classifier(cls2,vec_model)
    #print_positives_and_confidence(dataset,result171_dataset)

if __name__=='__main__':
    main()
