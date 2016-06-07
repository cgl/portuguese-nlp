# portuguese-nlp
Nlp work on Brazil Portuguese newswire text

You can see the dataset [here](http://mann.cmpe.boun.edu.tr/folha_data/)

You can find the reports [here](/docs/report_erc.md)

We have x number of newswire articles collected between years 1994-2016. We first apply some preprocessing to the dataset. Since the articles are in html format, we first clean the tags and rename all files such as:

    folca/data/2005/01/01/19.html --> folca/parsed-data/2005_01_01_19.html

and collect them all in one folder.

[Preprocessing on dataset](/dataset/README.md)


## More

* [brat Documentation!](/docs/brat.md)
* [Weka Documentation!](/docs/weka.md)
* [Some parsing with Stanford Parser](/docs/parse.md)
