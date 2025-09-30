import re, os, sys, csv
from urllib.parse import urlparse

def start_ehole():
    try:
        # 获取当前工作目录
        path_get = os.getcwd()
        
        # 首先读取bypass403_url.txt中的URL用于根目录扫描
        with open(os.path.join(path_get, "bypass403_url.txt"), 'r') as domains:
            domain_url = domains.read().strip()
        
        if not domain_url:
            print("错误: bypass403_url.txt为空")
            return
        
        # 创建临时文件用于扫描
        ehole_file = os.path.join(path_get, 'ehole', 'ehole.txt')
        open(ehole_file, 'w').close()  # 清空文件
        
        # 解析域名用于输出文件名
        parsed_url = urlparse(domain_url)
        domain1 = parsed_url.netloc
        domain1 = domain1.replace('.', '_').replace(':', '_')
        
        # 确保reports目录存在
        reports_dir = os.path.join(path_get, 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        try:
            # 尝试执行正常扫描逻辑（读取dir_file_path.txt和CSV文件）
            print("尝试执行正常扫描...")
            
            # 读取dir_file_path.txt
            if os.path.exists('dir_file_path.txt'):
                with open('dir_file_path.txt') as f:
                    f1 = f.read().strip()
                
                # 读取扫描结果文件中的URL
                if f1 and os.path.exists(f1):
                    with open(f1) as d:
                        d1 = d.readlines()
                    for dd in d1:
                        dd = dd.replace('\n', '').replace('\r', '')
                        if "404   " not in dd and ' 0B ' not in dd:
                            reg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                            url = re.findall(reg, dd)
                            try:
                                with open(ehole_file, 'a+') as ehole:
                                    ehole.write(url[0] + '\n')
                            except:
                                pass
            
            # 尝试读取CSV文件中的URL
            csv_file = os.path.join(reports_dir, domain1 + '.csv')
            if os.path.exists(csv_file):
                file_csv = open(csv_file, 'r', encoding='GB18030')
                rows = csv.reader(file_csv)
                for row in rows:
                    if len(row) > 0 and 'http' in row[0]:
                        try:
                            with open(ehole_file, 'a+') as ehole:
                                ehole.write(row[0] + '\n')
                        except:
                            pass
            
            # 检查是否有正常扫描到的URL
            with open(ehole_file, 'r') as f:
                urls = f.read().strip()
                
            # 如果正常扫描没有找到任何URL，或者文件不存在，则只扫描根目录
            if not urls:
                raise FileNotFoundError("目录扫描未发现路径")
                
        except FileNotFoundError as e:
            print(f"[提示]: {str(e)}，将只扫描根目录的指纹")
            # 只写入根URL到临时文件
            with open(ehole_file, 'w') as f:
                f.write(domain_url + '\n')
        
        # 根据操作系统类型执行不同命令
        win_mac = sys.platform
        if win_mac == "darwin":  # macOS
            print(f"正在扫描指纹: {domain_url}")
            # 确保ehole可执行
            os.system(f'chmod +x {os.path.join(path_get, "ehole", "ehole")}')
            # 执行ehole扫描
            os.system(f"{os.path.join(path_get, 'ehole', 'ehole')} finger -l {ehole_file}")
        elif win_mac == "win32":  # Windows
            os.system(f'{os.path.join(path_get, "ehole", "ehole.exe")} finger -l {ehole_file} -o {os.path.join(reports_dir, f"{domain1}.json")}')
        else:  # Linux或其他系统
            print(f"正在扫描指纹: {domain_url}")
            os.system(f'chmod +x {os.path.join(path_get, "ehole", "ehole")}')
            os.system(f"{os.path.join(path_get, 'ehole', 'ehole')} finger -l {ehole_file}")
        
        print(f"指纹扫描完成！")
        
    except Exception as e:
        print(f"扫描过程中发生错误: {str(e)}")
        # 错误发生时，也只扫描根目录的指纹
        try:
            path_get = os.getcwd()
            with open(os.path.join(path_get, "bypass403_url.txt"), 'r') as domains:
                domain_url = domains.read().strip()
            
            if domain_url:
                print(f"尝试只扫描根目录的指纹: {domain_url}")
                ehole_file = os.path.join(path_get, 'ehole', 'ehole.txt')
                with open(ehole_file, 'w') as f:
                    f.write(domain_url + '\n')
                
                win_mac = sys.platform
                if win_mac == "darwin":
                    os.system(f'chmod +x {os.path.join(path_get, "ehole", "ehole")}')
                    os.system(f"{os.path.join(path_get, 'ehole', 'ehole')} finger -l {ehole_file}")
                elif win_mac == "win32":
                    os.system(f'{os.path.join(path_get, "ehole", "ehole.exe")} finger -l {ehole_file}')
                else:
                    os.system(f'chmod +x {os.path.join(path_get, "ehole", "ehole")}')
                    os.system(f"{os.path.join(path_get, 'ehole', 'ehole')} finger -l {ehole_file}")
        except Exception as inner_e:
            print(f"尝试只扫描根目录指纹时也发生错误: {str(inner_e)}")