import re,os,sys,csv
from urllib.parse import urlparse

def start_ehole():
    path_get=os.getcwd()
    open(path_get+'/ehole/ehole.txt','w').close()
    with open('dir_file_path.txt') as f:
        f1=f.read()

    with open(f1) as d:
        d1=d.readlines()
    for dd in d1:
        dd=dd.replace('\n','').replace('\r','')
        reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url=re.findall(reg,dd)
        try:
            with open(path_get+'/ehole/ehole.txt','a+') as ehole:
                ehole.write(url[0]+'\n')
        except:
            pass

    try:
        with open("bypass403_url.txt",'r') as domains:
            domian=domains.read()
        parsed_url = urlparse(domian)
        domain1 = parsed_url.netloc
        file_csv = open("reports/" + domain1 + '.csv', 'r', encoding='GB18030')
        rows = csv.reader(file_csv)
        for row in rows:
            if 'http' in row[0]:
                try:
                    with open(path_get + '/ehole/ehole.txt', 'a+') as ehole:
                        ehole.write(row[0] + '\n')
                except:
                    pass
    except:
        pass
    win_mac=sys.platform
    if win_mac =="darwin":
        os.system(f'cd {path_get}/ehole/ && chmod 777 ehole')
        os.system(f"{path_get}/ehole/ehole finger -l {path_get}/ehole/ehole.txt")
    if win_mac == "win32":
        pass
