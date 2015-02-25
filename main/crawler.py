from BeautifulSoup import BeautifulSoup
import urllib2,codecs
"""
url = "http://www1.folha.uol.com.br/fsp/dinheiro/fi28079905.htm"
url = "http://www1.folha.uol.com.br/fsp/cotidiano/153605-carnaval-do-rio-tera-parodia-de-marchinhas-em-tom-de-protesto.shtml"
url = "http://www1.folha.uol.com.br/fsp/poder/87093-site-do-governo-e-invadido-em-protesto-contra-genoino.shtml"
"""

def read_file_gen(filename):
    with codecs.open(filename,"rU","utf-8") as infile:
        while 1:
            line = infile.readline()
            if not line:
                break
            yield line

def crawl(filename):
    url_gen = read_file_gen(filename)
    for url in url_gen:
        response = urllib2.urlopen(url)
        page = BeautifulSoup(response.read())
        try:
            page.findAll("td")[-2].findAll("p")[-1]
        except IndexError:
            page.find("div", {"id": "articleNew"})
