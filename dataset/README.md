# portuguese-nlp
Nlp work on Brazil Portuguese newswire text


### Dataset

Number of news per year:

```bash
  for year in `ls /ai/home/acelebi/folca/data`;
    do
      count=`find /ai/home/acelebi/folca/data/$year -type f -name '*.html' | wc -l` ;
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

Test clean:

    python classification/main/clean.py --check_dir /tmp/brazil/data/2012/03
    python classification/main/clean.py --raw_dir /tmp/brazil/data/2012/03 --parsed_dir /tmp/03/
    

Run parse:

```bash
  for year in `ls /tmp/brazil/data`;
    do 
      for month in `ls /tmp/brazil/data/$year`
        do 
          mkdir -p /tmp/brazil/parsed_data/$year/$month; 
          python classification/main/clean.py --raw_dir /tmp/brazil/data/$year/$month --parsed_dir /tmp/brazil/parsed_data/$year/$month; 
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

## logs

    cp -r /ai/home/acelebi/folca/data /tmp/brazil/
    tar -zcpf /tmp/brazil/raw_data.tar.gz /tmp/brazil/data
    # on TerraNova
    scp guest7@balina.ku.edu.tr:/tmp/brazil/raw_data.tar.gz ~/brazil/
    tar xzf ~/brazil/raw_data.tar.gz -C ~/brazil/
    
