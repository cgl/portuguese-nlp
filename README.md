# portuguese-nlp
Nlp work on Brazil Portuguese newswire text


### Tokenization and Parsing

Some bash scripting for lxparser:

```bash
  for file in $(find data/input/ -type f -printf "%f\n");
    do
      cat data/input/$file | Tokenizer/Tokenizer/run-Tokenizer.sh > data/tokenized/$file ;
    done
```

Some java for parsing:

  for file in $(find data/tokenized/ -type f -printf "%f\n");
      do
  	    java -Xmx1000m -cp stanford-parser-2010-11-30/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat oneline -uwModel edu.stanford.nlp.parser.lexparser.BaseUnknownWordModel cintil.ser.gz data/tokenized/$file > data/parsed/$file 2>>data/log_parse.txt ;
      done
