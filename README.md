# portuguese-nlp
Nlp work on Brazil Portuguese newswire text

You can browse [the dataset online](http://mann.cmpe.boun.edu.tr/folha_data/) and [see annotations on drive ](https://docs.google.com/spreadsheets/d/1TBNl7NblA2Ykz1VneMGfvcL8cHkZGpl58aup3gh2E9U/edit?usp=sharing)

We have x number of newswire articles collected between years 1994-2016. After preprocessing the dataset, since the articles are in html format, we first clean the tags and rename all files such as:

    folca/data/2005/01/01/19.html --> folca/parsed-data/2005_01_01_19.html

and collect them all in one folder.

- [1. Preprocessing on dataset](/dataset/README.md)
- [2. Crawling and Organizing the Training Set](/docs/training_set_preperation.md)
- [3. Classification by Graphlab](/docs/classification_with_graphlab.md)
- [4. Reports](/docs/report_erc.md)

## More

* [brat Documentation!](/docs/brat.md)
* [Weka Documentation!](/docs/weka.md)
* [Some parsing with Stanford Parser](/docs/parse.md)
