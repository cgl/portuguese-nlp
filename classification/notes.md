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


