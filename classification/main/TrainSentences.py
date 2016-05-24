from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from pprint import pprint
from gensim.models import word2vec
import re

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
        #import ipdb ; ipdb.set_trace()

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
