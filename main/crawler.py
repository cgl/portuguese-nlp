from BeautifulSoup import BeautifulSoup
import codecs,traceback
from urllib2 import HTTPError,urlopen
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

def crawl(filename,pages):
    url_gen = read_file_gen(filename)
    for url in url_gen:
        try:
            response = urlopen(url)
            page = BeautifulSoup(response.read())
            if page:
                pages.append(page)
            else:
                print("Empty page: %s" % url)
        except HTTPError:
            print(url)
            traceback.print_exc()

def parse_html(page):
    try:
        content = page.findAll("td")[-2].findAll("p")[-1]
    except IndexError:
        try:
            content = page.find("div", {"id": "articleNew"})
        except:
            traceback.print_exc()
            return None
    return content

def parse_pages(pages,training,test,label):
    i = 0
    for page in pages:
        content = parse_html(page)
        if page is not None:
            if i<2:
                test.append((content,label))
            else:
                training.append((content,label))
            i = (i + 1) % 3
