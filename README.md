# portuguese-nlp
Nlp work on Brazil Portuguese newswire text


### Tokenization and Parsing

We used [LX Parser](http://lxcenter.di.fc.ul.pt/tools/en/LXParserEN.html), a Constituency Parser for Portuguese based on [Stanford Parser](http://nlp.stanford.edu/software/lex-parser.shtml) and [LX-Tokenizer](http://lxcenter.di.fc.ul.pt/tools/en/LXTokenizerEN.html) to tokenize input prior to parsing.

Some bash scripting for LX-Tokenizer:

```bash
  for file in $(find data/input/ -type f -printf "%f\n");
    do
      cat data/input/$file | Tokenizer/Tokenizer/run-Tokenizer.sh > data/tokenized/$file ;
    done
```

Some java for parsing:

```bash
  for file in $(find data/tokenized/ -type f -printf "%f\n");
      do
  	    java -Xmx1000m -cp stanford-parser-2010-11-30/stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat oneline -uwModel edu.stanford.nlp.parser.lexparser.BaseUnknownWordModel cintil.ser.gz data/tokenized/$file > data/parsed/$file 2>>data/log_parse.txt ;
      done
```

Example parser output is:

```lisp
(ROOT
  (S
    (S
      (S
        (NP
          (ART A)
          (N' (N greve) (PP (P de_) (NP (ART os) (N' (N vigilantes) (PP (P de_) (NP (ART o) (N Rio)))))))
        )
        (VP
          (VP (V est?) (VP (V suspensa) (PP (P de) (ADV hoje))))
          (PP (P at?) (NP (N' (N segunda-feira) (A .*/))))
        )
      )
      (S
        (NP (ART A) (N decis?o))
        (VP (V foi) (VP (V tomada) (AP (ADV ontem) (A ,*/))))
      )
    )
    ...
```
