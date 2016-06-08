# Classification using Graphlab

Once the training data is ready in 

      python classification/main/graphlab_train.py --training_dir classification/data/v5/
      python classification/main/graphlab_train.py --dataset_dir /tmp/temp/
      
      python classification/main/graphlab_classify.py --dataset_dir my_dataset_2005


# Embeddings

[Word Embeddings](https://github.com/erickrf/nlpnet/blob/master/docs/models.rst#word-embeddings-portuguese) (Portuguese)

      pip install nlpnet
      wget http://nilc.icmc.usp.br/nlpnet/data/embeddings-pt.tgz
      tar xzf embeddings-pt.tgz
      
      python classification/embeddingstotxt.py --type plain --embeddings ~/brazil/w2e-embeddings/types-features.npy -v  ~/brazil/w2e-embeddings/vocabulary2.txt -o /tmp/
      mv /tmp/models.txt ~/brazil/portuguese-nlp/word2vec_model.txt

For more info [Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese](http://link.springer.com/article/10.1186/s13173-014-0020-x)
      
