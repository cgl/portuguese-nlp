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

    python classification/main/clean.py --raw_dir /tmp/brazil/data/2012/03 --parsed_dir /tmp/03/
