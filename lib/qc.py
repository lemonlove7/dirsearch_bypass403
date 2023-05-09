import os
import re
import tldextract
from colorama import init, Fore, Style
re_lists=[]

init()
def pass403_qc():
    urls=[]
    try:
        print(Fore.GREEN + Style.BRIGHT +'\nRemove invalid results with the same page length'+Style.RESET_ALL)
        with open('bypass403_url.txt') as f:
            url = f.read()
        urls.append(url)
        with open('jsfind403list.txt') as js_f:
            js_url=js_f.readlines()
        for js_i in js_url:
            js_i=js_i.replace('\n','').replace('\r','')
            urls.append(js_i)

        for url1 in urls:
            file_domain = tldextract.extract(url1).domain
            with open(file_domain + '.txt') as f:
                f1 = f.readlines()
            for i in f1:
                i = i.replace('\n', '').replace('\r', '')
                if 'Header= {' in i:
                    re_i = re.findall('SIZE: (.*?)---Header=', i)
                    re_str = "".join(re_i)
                if 'Header= {' not in i:
                    re_str = i[i.rfind('SIZE: '):]
                if re_str != '':
                    re_lists.append(re_str)
            list2 = list(set(re_lists))

            for ii in list2:
                for p in f1:
                    p = p.replace('\n', '')
                    if ii in p:
                        if "---Header= {" in p:
                            p = p.replace('---', '\n')
                            p = p+'\n'
                        if "STATUS: 403" in p:
                            pass
                        elif "STATUS: 404" in p:
                            pass
                        else:
                            print(p)
                        break
            os.remove(file_domain + '.txt')
    except:
        pass
