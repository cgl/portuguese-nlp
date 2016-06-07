# Crawling and Preparing Training Set

Usage

Below gives the raw pages as a list:

    from main import crawler
    pages = [] ; crawler.crawl("data/relevant.txt",pages)

And this is how to parse the html pages once you have raw pages as html in list pages:

    training = [] ; test = []
    label = True
    crawler.parse_pages(pages,training,test,label)

This is the command line code for testing:

    cd classification/
    python main/crawler.py --class_irr data/urls/irrelevant.txt --class_rel data/urls/relevant.txt --output_dir data/test

If you want to add new documents:

    cd classification/
    python main/crawler.py --class_irr data/urls/development_irr.txt --class_rel data/urls/development_rel.txt --output_dir data/test_24_may
    
Clean the documents:

    python main/clean.py --check_dir data/test_24_may/raw
    python main/clean.py --raw_dir data/test_24_may/raw --parsed_dir data/test_24_may/parsed


Try [Weka Documentation!](/docs/weka.md)

Some bash:

    cd ~/Downloads/Duru05/full_main/
    for a in [1-5]*.ann; do   echo $a;  mv $a `printf d%04d.%s ${a%.*} ${a##*.}`; done
    for a in [1-5]*.txt; do   echo $a;  mv $a `printf d%04d.%s ${a%.*} ${a##*.}`; done
    for a in d[0-5]*.txt.ann; do   echo $a; mv $a `printf %s.%s ${a%.*.*} ${a##*.}` ; done
    for a in d[0-5]*.txt.txt; do   echo $a;  mv $a `printf %s.%s ${a%.*.*} ${a##*.}` ; done

    cp -r ~/work/portuguese-nlp/classification/data/v1/parsed/v4/class_irr ~/work/portuguese-nlp/classification/data/v5/
    mkdir ~/work/portuguese-nlp/classification/data/v5/class_rel
    find ~/Downloads/Duru05/full_main/ -name "*.txt" -exec cp {} ~/work/portuguese-nlp/classification/data/v5/class_rel/ \;
