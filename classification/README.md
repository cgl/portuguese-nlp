# portuguese-nlp
Nlp work on Brazil Portuguese newswire text


Usage

Below gives the raw pages as a list:

from main import crawler
pages = [] ; crawler.crawl("data/relevant.txt",pages)

And this is how to parse the html pages once you have raw pages as html in list pages:

training = [] ; test = []
label = True
crawler.parse_pages(pages,training,test,label)

This is the command line code for testing:

python main/crawler.py --class1 data/test/relevant.txt --class2 data/test/irrelevant.txt --output data/test

Try [Weka Documentation!](docs/weka.md)
