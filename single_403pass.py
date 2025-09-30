from lib.pass403 import Arguments,Program
from lib.qc import pass403_qc
import argparse


def bypass(url,path):
    try:
        argument = Arguments(url, None, path, None)
        program = Program(argument.return_urls(), argument.return_dirs())
        program.initialise()
    except:
        pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='help')
    parser.add_argument("-u", "--url", help="url", default='')
    parser.add_argument("-p", "--path", help="url path", default='')
    args = parser.parse_args()
    url=args.url
    with open('bypass403_url.txt','w') as f:
        f.write(url)
    path=args.path
    bypass(url,path)
    pass403_qc()

