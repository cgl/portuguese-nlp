import numpy as np
import argparse, cPickle, codecs, os

def read_plain_embeddings(filename):
    """
    Read an embedding from a plain text file with one vector per 
    line, values separated by whitespace.
    """
    with open(filename,
 'rb') as f:
        text = f.read().strip()
    
    text = text.replace('\r\n', '\n')
    lines = text.split('\n')
    #import ipdb ; ipdb.set_trace()
    matrix = np.array([[float(value) for value in line.split()]
                       for line in lines])
    
    return matrix


def read_w2e_embeddings(filename):
    """
    Load the feature matrix used by word2embeddings.
    """
    with open(filename, 'rb') as f:
        model = cPickle.load(f)
    matrix = model.get_word_embeddings()

    # remove <s>, </s> and <padding>
    matrix = np.append([matrix[0]], matrix[4:], axis=0)
    new_vectors = nlpnet.utils.generate_feature_vectors(2,
                                                        matrix.shape[1])
    matrix = np.append(matrix, new_vectors, axis=0)
    return matrix

def read_plain_vocabulary(filename):
    """
    Read a vocabulary file containing one word type per line.
    Return a list of word types.
    """
    words = []
    with open(filename, 'rb') as f:
        for line in f:
            word = unicode(line, 'utf-8').strip()
            if not word:
                continue
            words.append(word)
    
    return words

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('type', help='Format of the embeddings. See the description below.', 
                        choices=['plain', 'senna', 'gensim', 'word2embeddings', 'single', 'polyglot'])
    parser.add_argument('embeddings', help='File containing the actual embeddings')
    parser.add_argument('-v', help='Vocabulary file, if applicable. '\
                        'In SENNA, it is hash/words.lst', dest='vocabulary')
    parser.add_argument('-o', help='Directory to save the output', default='.',
                        dest='output_dir')
    args = parser.parse_args()
    if args.type == 'plain':
        words = read_plain_vocabulary(args.vocabulary)
        matrix = np.load(args.embeddings)
        #read_plain_embeddings(args.embeddings)
    vocab = words
    with codecs.open(os.path.join(args.output_dir,'model.txt'), 'w' , 'utf-8') as output:
        output.write("%s %s\n" %matrix.shape)
        for index in range(0,len(words)):
            vector = list()
            for dimension in matrix[index]:
                vector.append(str(dimension))
                vector_str = " ".join(vector)
                line = words[index] + " "  + vector_str
            output.write(line + "\n")
    """
    import nlpnet
    nlpnet.set_data_dir(args.output_dir)
    wd = nlpnet.word_dictionary.WordDictionary.init_from_wordlist(words)
    wd.save()
    """
"""
https://github.com/erickrf/nlpnet/blob/master/bin/nlpnet-load-embeddings.py

"""
