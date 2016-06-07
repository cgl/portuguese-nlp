# portuguese-nlp
Nlp work on Brazil Portuguese newswire text

## Reports

### Workers Protests

![Alt text](relative/path/to/img.jpg?raw=true "Title")

### Workers Protests
Events marked as strikes are classified as workers protests.

### Total Number of Events
The distribution of all events in years.

### Protest Events
The distribution of protes events in years.

### Leftwing Events
The distribution of leftwing events in years.

### Rural/Peasant Events
The events occoured in rural places or organized by peasants.
* organizer can be CMS
* participant can be peasant or rural worker

## Project

You can see the dataset [here](http://mann.cmpe.boun.edu.tr/folha_data/)

We have x number of newswire articles collected between years 1994-2016. We first apply some preprocessing to the dataset. Since the articles are in html format, we first clean the tags and rename all files such as:

    folca/data/2005/01/01/19.html --> folca/parsed-data/2005_01_01_19.html

and collect them all in one folder.

[Preprocessing on dataset](/dataset/README.md)


## More

* [brat Documentation!](/docs/brat.md)
* [Weka Documentation!](/docs/weka.md)
* [Some parsing with Stanford Parser](/docs/parse.md)
