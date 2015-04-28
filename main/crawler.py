from BeautifulSoup import BeautifulSoup
import codecs,traceback,sys,os,io

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
#  writes parsed html pages to files
def parsed_run(url_gen,label,folder):
    pages = []
    crawl(url_gen,pages)
    training = []
    test = []
    parse_pages(pages,training,test,label)
    write_to_file(training,folder+"/training/class_"+label)
    write_to_file(test,folder+"/test/class_"+label)

#  writes raw html pages to files
def run_raw(url_gen,label,folder):
    sys.stdout.write("Working on class [%s]...\n" %label)
    pages = []
    crawl(url_gen,pages)
    write_to_file(pages,folder+"/raw/class_"+label)

def write_to_file(list_pages,directory):
    sys.stdout.write("Starting [Writing to File]...\n")
    if not os.path.exists(directory):
        os.makedirs(directory)
    for ind,page in enumerate(list_pages):
        with io.open(os.path.join(directory,str(ind)+".txt"), 'w') as outfile:
            if type(page) is tuple:
                page = page[0]
            outfile.write(page.renderContents().decode('utf-8'))
    sys.stdout.write("Completed [Writing to File]...\n")

#url_gen = read_file_gen(filename)
def crawl(url_gen,pages):
    sys.stdout.write("Starting [Crawling]...\n")
    for url in url_gen:
        try:
            response = urlopen(url.strip())
            if response.code == 200:
                page = BeautifulSoup(response.read().decode('utf-8', 'ignore'))
                if not page:
                    page = BeautifulSoup("Empty page at <a href='%s'>%s</a>" %(url,url))
                    sys.stdout.write("Empty page at %s\n" % url)
            else:
                page = BeautifulSoup("HTTP Code %i received at <a href='%s'>%s</a>" %(response.code,url,url))
                sys.stdout.write("HTTP Code %i received at <a href='%s'>%s</a>" %(response.code,url,url))
        except HTTPError:
            #traceback.print_exc()
            #traceback.print_tb(sys.exc_traceback, limit=1, file=sys.stdout)
            formatted_lines = traceback.format_exc().splitlines()
            sys.stderr.write("%s at %s" %(formatted_lines[-1],url.strip()))
            page = BeautifulSoup("HTTP Error 404: Not Found at <a href='%s'>%s</a>" %(url,url))
        pages.append(page)
    sys.stdout.write("Completed [Crawling]...\n")

def parse_html(page):
    try:
        tds = page.findAll("td")
        content = tds[-2] # throws IndexError if tds empty
        for td_ind in range(1,len(tds)):
            content = tds[-1*td_ind]
            if content.find("b"):
                #print(-1*td_ind)
                break
        table = page.find("table", {"id": "main"})
        if table is None:
            pass
            #print("----------------------")
        else:
            tds2 = table.findAll("td")
            content2 = tds2[-2]
            for td_ind in range(1,len(tds2)):
                content2 = tds2[-1*td_ind]
                if content2.find("b"):
                    #print(-1*td_ind)
                    break
            #if content != content2:
                #print(tds2)
                #print("*******************")
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

from subprocess import check_output
def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

import argparse
def main():
    parser = argparse.ArgumentParser(description = "Analysis scripts for LexNorm in W-NUT 2015")
    parser.add_argument("--class1", required = True, type=read_file_gen, help = "A text file: Urls of the True class files")
    parser.add_argument("--class2", required = True, type=read_file_gen, help = "A text file: Urls of the False class files")
    parser.add_argument("--output_dir", required = False, default="data" ,type=str , help = "Output Dir")
    args = parser.parse_args()
    #print(args.class1)
    run_raw(args.class1,"rel",args.output_dir)
    run_raw(args.class2,"irr",args.output_dir)

if __name__ == "__main__":
    main()
