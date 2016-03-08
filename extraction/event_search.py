import argparse

def extract_event(filename):
    lines = []
    with open(filename) as file:
        for  line in file.readlines():
            if not line.startswith("SENTENCE_SKIPPED"):
                lines.append(line)
                if line.find("greve") >= 0:
                    print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--root', default='document', help='The document root')
    parser.add_argument('-f', '--file', default='document', help='The input parse tree')
    opts = parser.parse_args()
    opts.root = opts.root.decode('utf8')

    extract_event(opts.file)
