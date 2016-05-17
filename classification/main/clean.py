# encoding=utf-8
# Author Cagil
# Edit 28 Apr 2015
# Edit Log 21 Oct 2015
# Unescape added, it is optional
import argparse,os,sys,io,traceback, codecs
from BeautifulSoup import BeautifulSoup,Comment
UNESCAPE = True
import HTMLParser
h = HTMLParser.HTMLParser()
def main():
    parser = argparse.ArgumentParser(description = "Parses & removes unnecessary html tags from raw classifier files")
    parser.add_argument("--raw_dir", required = False, default=None ,type=str ,
                        help = "Raw data dir. Should include at least one label folder. eg. irr/ or rel/ ")
    parser.add_argument("--parsed_dir", required = False, default=None ,type=str , help = "Parsed data dir")
    #parser.add_argument("--clean", required = False, default=False ,type=bool , help = "Output Dir")
    parser.add_argument("--divide", required = False, default=False,action='store_false', dest='boolean_switch',
                        help = "Parsed data dir")
    parser.add_argument("--debug", required = False, default=False,action='store_true', dest='debug',
                        help = "Parsed data dir")
    parser.add_argument("--check_dir", required = False, default=None ,type=str , dest='check_dir',
                        help = "given a nested directory name checks if the files inside is Portuguese")

    args = parser.parse_args()
    #print(args.class1)
    if args.raw_dir and args.parsed_dir:
        if os.path.exists(args.raw_dir): # and os.path.exists(args.parsed_dir):
            get_pages(args.raw_dir,args.parsed_dir,args.boolean_switch,debug=args.debug)
        else:
            print("No such directory")
    elif args.check_dir:
        if os.path.exists(args.check_dir):
            print("Checking directory %s" %args.check_dir)
            check_encoding(args.check_dir)
        else:
            print("No such directory")
    else:
        sys.stderr.write("Error")

# given a nested directory name checks if the files inside is Portuguese
def check_encoding(input_dir):
    count=0
    for dirname,_,filenames in os.walk(input_dir):
      for filename in filenames:
        full_name = os.path.join(dirname,filename)
        content = []
        if os.path.getsize(fpath) > 0:
            check_encoding_file(full_name)
        else:
            print("%s is empty" %(full_name))
        count+=1
    print("Checked %s files" %count)

def check_encoding_file(full_name):
    if not full_name.endswith(".DS_Store") and not full_name.endswith(".meta"):
        with codecs.open(full_name,"r","utf-8") as inputfile:
        #with io.open(full_name,"r") as inputfile:
            try:
                content = inputfile.read()
                if check_encoding_string(h.unescape(content)):
                    UNESCAPE = True
                elif check_encoding_string(h.unescape(content.encode("latin1"))):
                    LATIN = True
                    print("%s is Latin encoded" %(full_name))
                else:
                    print("%s is not Portuguese" %(full_name))
                    return False
            except UnicodeDecodeError:
                pass #print("Couldn't read %s" %full_name)
        return True

def check_encoding_string(content):
    if max(content.count(u"í"),content.count(u"á"), content.count(u"é"), content.count(u"ã")) < 1:
        return False
    return True

def get_pages(raw_dir,parsed_dir,divide,debug=False):
    classes = gen_walk(raw_dir)
    for label,sub_path in classes.items():
        i = 0 ; path = ""
        create_dirs(parsed_dir,label,divide)
        for raw_filename in gen_walk_inner(sub_path):
            if raw_filename.startswith(".") or raw_filename.endswith(".meta"):
                  continue
            if divide:
                path = "test"  if i < 1 else "training"
                i = (i + 1) % 4 #2
            infilename = os.path.join(raw_dir,label,raw_filename)
            outfilename = os.path.join(parsed_dir,path,label,raw_filename)
            write_parsed_page_alt(infilename,outfilename,debug=debug)
            #write_parsed_page(infilename,outfilename,debug=debug)
        sys.stdout.write("Last file for [%s] written to file: %s\n" %(label,outfilename))
        #sys.stdout.write("Completed [Writing to File: %s]\n" %label)

def write_parsed_page_alt(infilename,outfilename,debug=False):
    content,title = parse_page_alternative(infilename)
    if content is None or content is u"":
        sys.stderr.write("Empty result return for %s.\n" %infilename)
        return
    if check_encoding_string(content):
        pass
    elif check_encoding_string(content.encode("latin1")):
        content = content.encode("latin1")
        title = title.encode("latin1")
    elif not check_encoding_string(content):
        if debug:
            print("File is not Portuguese %s" %infilename)
            print("[DELETED CONTENT] %s\n" %content)
        return
    write_to_file(outfilename,title,content)
    if debug:
        print("[CLEANED CONTENT] %s\n" %content)
        #sys.stdout.write("[UNICODE CONTENT] %s\n" %unicode_content)
        #sys.stdout.write("[INFILENAME]%s\n" %infilename)
        sys.stdout.write("[OUTFILENAME]%s\n" %outfilename)
        sys.stdout.write("************************************************************\n")
        sys.stdout.write("************************************************************\n")

def parse_page_alternative(infilename):
    page = get_soup_page(infilename)
    title = get_title(page,infilename)
    clean_page(page)
    clean_more(page)
    #value = unicode(page.find("body"))
    try:
        value = page.find("body").getText()
    except AttributeError:
        traceback.print_exc()
        sys.stderr.write("No body in %s\n" %infilename)
        return None,None
    content_raw = ''.join(BeautifulSoup(value, convertEntities=BeautifulSoup.HTML_ENTITIES).findAll(text=True))
    list = content_raw.split("\n")
    content = "\n".join([line for line in list if line.strip() is not u"" and len(line.split(" ")) > 3 ])
    return content,title

def get_soup_page(infilename):
    try:
        with io.open(infilename, 'r') as infile:
            page = BeautifulSoup(infile)
    except:
        with io.open(infilename, 'r',encoding="latin1") as infile:
            page = BeautifulSoup(infile)
    return page

def write_to_file(outfilename,title,content):
    try:
        with io.open(outfilename, 'w') as outfile:
            if UNESCAPE:
                title = h.unescape(title)
                content = h.unescape(content)
            outfile.write("%s\n" %title)
            outfile.write(content)
    except TypeError:
        traceback.print_exc()
        sys.stderr.write("Couldn't write %s" %outfilename)

def get_title(page,infilename): # can get rid of infilename and exceptions
    try:
        title = page.find("title").getText().strip(u"Folha de S.Paulo").strip("-").strip()
    except AttributeError:
        traceback.print_exc()
        sys.stderr.write("Title AttributeError at %s\n" %infilename)
        title = u" "
    except TypeError:
        sys.stderr.write("Title TypeError at %s\n" %infilename)
        title = u" "
    return title

def clean_page(page):
    scripts = page.findAll("script")
    [scr.extract() for scr in scripts]
    comments = page.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

def clean_more(page):
    imgs = page.findAll("img")
    [img.extract() for img in imgs]
    brs = page.findAll("br")
    [br.extract() for br in brs]
    links = page.findAll("a")
    [link.extract() for link in links]
    comments = page.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

def gen_walk(path):
    classes = {}
    for dirname, dirnames, _ in os.walk(path):
        # print path to all subdirectories first.
        for class_name in dirnames:
            sub_path = os.path.join(dirname, class_name)
            classes[class_name] = sub_path
    return classes

def gen_walk_inner(sub_path):
    for _, _, filenames in os.walk(sub_path):
        if '.DS_Store' in filenames:
            # don't go into any .git directories.
            filenames.remove('.DS_Store')

        for filename in filenames:
            yield filename # os.path.join(sub_dirname, filename)


def create_dirs(parsed_dir,label,divide):
    if divide:
        directory = os.path.join(parsed_dir,"test",label)
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(os.path.join(parsed_dir,"training",label))
    else:
        directory = os.path.join(parsed_dir,label)
        if not os.path.exists(directory):
            os.makedirs(directory)

###########################

def parse_page(infilename):
    page = get_soup_page(infilename)
    title = get_title(page,infilename)
    clean_page(page)
    content = parse_html(page)
    try:
        clean_more(content)
    except AttributeError:
        sys.stderr.write("Content gives Att Error, %s\n" %infilename)
        return None,None
    return content.text.strip("|\n ?"),title

def parse_html(page):
    try:
        table = page.find("table", {"id": "main"})
        if table is not None:
            page = table
    except:
        print("***************")
    try:
        tds = page.findAll("td")
        content = tds[-2] # throws IndexError if tds empty
        for td_ind in range(1,len(tds)):
            content = tds[-1*td_ind]
            if content.find("b"):
                #print(-1*td_ind)
                break
    except IndexError:
        try:
            content = page.find("div", {"id": "articleNew"})
        except:
            sys.stderr.write("Error line 56")
            return None
    return content

def write_parsed_page(infilename,outfilename,debug=False):
    content,title = parse_page(infilename) # may be empty
    if content is None:
        sys.stdout.write("Trying other way around for %s\n" %infilename)
        content,title = parse_page_alternative(infilename)
        if content is None or content is u"":
            sys.stderr.write("Empty result return for %s.\n" %infilename)
            return
    write_to_file(outfilename,title,content)
    if debug:
        sys.stdout.write("[CLEANED CONTENT] %s\n" %content)
        #sys.stdout.write("[UNICODE CONTENT] %s\n" %unicode_content)
        sys.stdout.write("[INFILENAME]%s\n" %infilename)
        sys.stdout.write("[OUTFILENAME]%s\n" %outfilename)
        sys.stdout.write("************************************************************\n")
        sys.stdout.write("************************************************************\n")


if __name__ == "__main__":
    main()
