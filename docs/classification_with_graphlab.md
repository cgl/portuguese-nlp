# Classification using Graphlab

Previously : [Crawling and Preparing Training Set](/docs/training_set_preperation.md)

Once the training data is ready in 

    # Build the classifier
    python classification/graphlab/graphlab_train.py --training_dir classification/data/latest/
    # Build the dataset
    python classification/graphlab/graphlab_train.py --dataset_parsed_dir ~/brazil/2005_parsed/ # ~/brazil/all_files_parsed
    # Classify the dataset
    python classification/graphlab/graphlab_classify.py --dataset_dir graphlab/my_dataset_2005 --classified_dir graphlab/result_dataset
    #to print the results:
    python classification/graphlab/graphlab_classify.py --classified_dir result_dataset --print

Classification by event type:

    python classification/graphlab/classify_by_event_type.py --classified_dir graphlab/result_dataset
    python classification/graphlab/classify_by_event_type.py --print

    
# Embeddings

[Word Embeddings](https://github.com/erickrf/nlpnet/blob/master/docs/models.rst#word-embeddings-portuguese) (Portuguese)

      pip install nlpnet
      wget http://nilc.icmc.usp.br/nlpnet/data/embeddings-pt.tgz
      tar xzf embeddings-pt.tgz
      
      python classification/embeddingstotxt.py --type plain --embeddings ~/brazil/w2e-embeddings/types-features.npy -v  ~/brazil/w2e-embeddings/vocabulary2.txt -o /tmp/
      mv /tmp/models.txt ~/brazil/portuguese-nlp/word2vec_model.txt

For more info [Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese](http://link.springer.com/article/10.1186/s13173-014-0020-x)
      
