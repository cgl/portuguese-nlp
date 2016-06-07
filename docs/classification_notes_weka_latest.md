# WEKA

  
    echo /Library/Java/JavaVirtualMachines/jdk1.7.0_25.jdk/Contents/Home/bin/
    weka_home=/Applications/weka-3-6-12-oracle-jvm.app/Contents/Java ; export CLASSPATH=$CLASSPATH:$weka_home/weka.jar:$weka_home/libsvm.jar:$JAVA_HOME/bin
    cp /Applications/weka-3-6-12-oracle-jvm.app/Contents/Java/weka.jar ~/work/portuguese-nlp/classification/
    cd ~/work/portuguese-nlp/classification/
    java weka.classifiers.meta.FilteredClassifier -i -t data/versions/v18_parsed_str_all.arff \ 
      -F "weka.filters.unsupervised.attribute.StringToWordVector -R first-last -W 100 -prune-rate -1.0 -C -T -I -N 0 -L -S \
      -stemmer weka.core.stemmers.NullStemmer -M 1 -stopwords /Users/cagil/work/portuguese-nlp/stoplist.txt" \
      -W weka.classifiers.trees.RandomForest -- -I 70 -K 0 -S 1 -D
    
            === Detailed Accuracy By Class ===
      
                     TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                       0.967     0.074      0.931     0.967     0.949      0.982    class_irr
                       0.926     0.033      0.965     0.926     0.945      0.982    class_rel
      Weighted Avg.    0.947     0.054      0.948     0.947     0.947      0.982
      
      
      === Confusion Matrix ===
      
         a   b   <-- classified as
       499  17 |   a = class_irr
        37 463 |   b = class_rel


180 437 arası alakasız dosyalar çıkarıldıktan sonra.


    java weka.core.converters.TextDirectoryLoader -Dfile.encoding=utf-8  \
    -dir data/v2/parsed > data/versions/v19_parsed_str_all.arff

Old setting from v18, let's try it with v21(best f-measure setting so far)

    java weka.core.converters.TextDirectoryLoader -Dfile.encoding=utf-8  \
    > -dir data/v1/parsed/v2/ > data/versions/v20_parsed_str_all.arff
    
    java weka.classifiers.meta.FilteredClassifier -i -t data/versions/v20_parsed_str_all.arff  -F \
    "weka.filters.unsupervised.attribute.StringToWordVector -R first-last -W 60 -prune-rate -1.0 -C -T -I -N 0 -L -S \
    -stemmer weka.core.stemmers.NullStemmer -M 1 -stopwords stoplistv2.txt"  -W weka.classifiers.trees.RandomForest -- -I 70\
    -K 0 -S 1 -D #v29
    
    === Detailed Accuracy By Class ===
    
                   TP Rate   FP Rate   Precision   Recall  F-Measure   ROC Area  Class
                     0.971     0.064      0.94      0.971     0.955      0.984    class_irr
                     0.936     0.029      0.969     0.936     0.952      0.984    class_rel
    Weighted Avg.    0.954     0.047      0.954     0.954     0.954      0.984
    
    
    === Confusion Matrix ===
    
       a   b   <-- classified as
     501  15 |   a = class_irr
      32 467 |   b = class_rel


V3 is the V2 - 12 news that are does not include protest news.

    java weka.core.converters.TextDirectoryLoader -Dfile.encoding=utf-8  -dir data/v1/parsed/v3/ \
    > data/versions/v21_parsed_str_all.arff

