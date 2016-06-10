#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TrainSentences import txt2words

import os,io,traceback,codecs,argparse
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


def add_dev(sf,vec_model):
    dev_irr = "classification/data/v4_dev/class_irr/"
    dev_rel ="classification/data/v4_dev/class_rel/"
    sf = add_arguments(sf,dev_irr,0,vec_model)
    sf = add_arguments(sf,dev_rel,1,vec_model)
    return sf

def main():
    parser = argparse.ArgumentParser(description = "Trains a classifiers for news and saves it. Also it can build the dataset given the folder.")
    parser.add_argument("--dataset_dir", required = False, default=None ,type=str ,
                        help = "Dataset directory ex: /home/cagil/brazil/all_files_parsed/ ")
    parser.add_argument("--training_dir", required = False, default=None ,type=str ,
                        help = "Training directory with irr/ and rel/ folders ex: classification/data/v5/")

    args = parser.parse_args()
    if args.training_dir or args.dataset_dir:
        vec_model = word2vec.Word2Vec.load_word2vec_format('word2vec_model.txt',binary=False)
    if args.training_dir:
        irr_folder = os.path.join(args.training_dir,"class_irr")
        rel_folder = os.path.join(args.training_dir,"class_rel")
        sf = add_arguments(None,rel_folder,1,vec_model)
        sf = add_arguments(sf,irr_folder,0,vec_model)

        cls1 = train_classifier(sf)
        #test_classifier(cls1,vec_model)

        df = add_dev(sf,vec_model)
        df.save("my_training_dataset")
        cls2 = train_classifier(df)
        cls2.save("my_classifier")
    #builds dataset
    if args.dataset_dir:
        #dataset_folder = "/home/cagil/brazil/all_files_parsed/" #"/tmp/temp/"
        dataset_folder = args.dataset_dir
        dataset = add_arguments(None,dataset_folder,None,vec_model)
        dataset.save("my_dataset")

if __name__=='__main__':
    main()
