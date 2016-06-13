# portuguese-nlp
Nlp work on Brazil Portuguese newswire text


## 1. Preprocessing 

### Dataset

Number of news per year:

```bash
folder=~/brazil/data # /ai/home/acelebi/folca/data
for year in `ls $folder`;
  do
    count=`find $folder/$year -type f -name '*.html' | wc -l` ;
    printf "%s %s\n" $year $count ;
  done
  2004 7876
  2005 19368
  2006 18720
  2007 18579
  2008 19281
  2009 16337
  2010 24062
  2011 22372
  2012 25102
  2013 21714
  2014 20095
  2015 5526
```

### Preprocess

Test clean:

    python classification/main/clean.py --check_dir ~/brazil/data/2012/03
    python classification/main/clean.py --raw_dir ~/brazil/data/2012/03 --parsed_dir /tmp/03/

Run parse:

```bash
for year in `ls $folder`;
  do 
    for month in `ls $folder/$year`
      do 
        mkdir -p ~/brazil/parsed_data/$year/$month; 
        python classification/main/clean.py --raw_dir ~/brazil/data/$year/$month --parsed_dir ~/brazil/parsed_data/$year/$month; 
      done; 
  done
```

Merge folders

```bash
  mydir=~/brazil/
  cd $mydir/parsed_data/
  find . -name '*.html' -size +1024c -printf '%P\0' | pax -0rws ':/:_:g' ${mydir}/all_files_parsed
   ls ${mydir}/all_files_parsed/ | head
2005_01_01_0.html
2005_01_01_19.html
2005_01_01_1.html
2005_01_01_21.html
```

### logs

    cp -r /ai/home/acelebi/folca/data /tmp/brazil/
    tar -zcpf /tmp/brazil/raw_data.tar.gz /tmp/brazil/data
    # on TerraNova
    scp guest7@balina.ku.edu.tr:/tmp/brazil/raw_data.tar.gz ~/brazil/
    tar xzf ~/brazil/raw_data.tar.gz -C ~/brazil/
    
    data_root=/home/cagil/brazil
    year=2004
    for month in `ls $data_root/data/$year`;         
      do            
        mkdir -p /tmp/parsed_data/$year/$month;            
        python classification/main/clean.py --raw_dir $data_root/data/$year/$month --parsed_dir /tmp/parsed_data/$year/$month;          
      done;

Next is [2. Crawling and Preparing Training Set](/docs/training_set_preperation.md)

Back to [Main Page](/README.md)
