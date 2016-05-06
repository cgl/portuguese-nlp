import argparse,codecs

def extract_event(filename,keyword="protesto"):
    ''' Extracts events
    '''
    lines = []
    with codecs.open(filename,encoding="utf-8") as file:
        for  line in file.readlines():
            if not line.startswith("SENTENCE_SKIPPED"):
                if line.find(keyword) >= 0:
                    #print(line)
                    lines.append(line.strip())
    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='document', help='The document root')
    parser.add_argument('-f', '--file', default='document', help='The input parse tree')
    opts = parser.parse_args()
    opts.root = opts.root.decode('utf8')

    extract_event(opts.file)
