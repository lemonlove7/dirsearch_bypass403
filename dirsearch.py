#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

import time
from colorama import init, Fore, Style

from lib.pass403_optimized import OptimizedArguments as Arguments, OptimizedProgram as Program
from lib.qc import pass403_qc


import threading
from concurrent.futures import ThreadPoolExecutor
import queue


import sys,os

from pkg_resources import DistributionNotFound, VersionConflict

from lib.core.data import options
from lib.core.exceptions import FailedDependenciesInstallation
from lib.core.installation import check_dependencies, install_dependencies
from lib.core.settings import OPTIONS_FILE
from lib.parse.config import ConfigParser

init()

if sys.version_info < (3, 7):
    sys.stdout.write("Sorry, dirsearch requires Python 3.7 or higher\n")
    sys.exit(1)

config = ConfigParser()
config.read(OPTIONS_FILE)

if config.safe_getboolean("options", "check-dependencies", False):
    try:
        check_dependencies()
    except (DistributionNotFound, VersionConflict):
        option = input("Missing required dependencies to run.\n"
                       "Do you want dirsearch to automatically install them? [Y/n] ")

        if option.lower() == 'y':
            print("Installing required dependencies...")

            try:
                install_dependencies()
            except FailedDependenciesInstallation:
                print("Failed to install dirsearch dependencies, try doing it manually.")
                exit(1)
        else:
            config.set("options", "check-dependencies", "False")

            with open(OPTIONS_FILE, "w") as fh:
                config.write(fh)


##

def bypass():
    """优化的403bypass函数"""
    with open('bypass403_url.txt') as f:
        bypass403_url = f.read().strip()
    
    # 收集所有需要处理的路径
    paths_to_process = []
    while not q.empty():
        path_403 = q.get()
        paths_to_process.append(path_403)
    
    if not paths_to_process:
        return
    
    print(f"开始处理 {len(paths_to_process)} 个403路径")
    
    # 使用优化版本处理
    try:
        argument = Arguments(bypass403_url, None, None, None)
        program = Program(argument.return_urls(), paths_to_process, max_workers=20)
        program.initialise()
    except Exception as e:
        print(f"bypass处理出错: {e}")
        # 如果处理失败，尝试逐个处理
        for path_403 in paths_to_process:
            try:
                argument = Arguments(bypass403_url, None, path_403, None)
                program = Program(argument.return_urls(), argument.return_dirs())
                program.initialise()
            except:
                pass


def run_bypass403():
    import multiprocessing
    size = os.path.getsize('403list.txt')
    size_js=os.path.getsize('jsfind403list.txt')
    from lib.core.options import parse_options
    if (parse_options()['bypass']) == None:
        pass
    else:
        bp403="".join(parse_options()['bypass'])
        if bp403 =='yes':
            if size ==0 and size_js ==0:
                print(Fore.GREEN + Style.BRIGHT + 'No 403 status code present!'+Style.RESET_ALL)
            else:
                print(Fore.GREEN + Style.BRIGHT+'Start 403bypass!'+Style.RESET_ALL)
                print(Fore.CYAN + Style.BRIGHT + 'Using optimized 403bypass mode!'+Style.RESET_ALL)
                
                # 处理403list.txt路径
                with open('403list.txt',) as f1:
                    list_403=f1.readlines()
                for path_403 in list_403:
                    path_403=path_403.replace('\n','').replace('\r','')
                    q.put(path_403)
                
                # 使用优化的bypass函数
                bypass()

                # 处理jsfind403list.txt路径，使用优化模式
                if size_js > 0:
                    try:
                        with open('jsfind403list.txt') as js1:
                            jsf=js1.readlines()
                        
                        # 收集所有JS发现的URL和路径
                        js_urls = []
                        js_paths = []
                        
                        for ff in jsf:
                            ff = ff.replace('\n', '').replace('\r', '')
                            num_slashes = ff.count('/')
                            if num_slashes == 2:
                                ff = ff + '/'
                            split_url = ff.split("/")
                            js_url = "/".join(split_url[:3])
                            js_path = split_url[3]
                            if js_path == '':
                                js_path = '/'
                            
                            if js_url not in js_urls:
                                js_urls.append(js_url)
                            js_paths.append(js_path)
                        
                        # 使用优化模式处理JS发现的路径
                        if js_urls and js_paths:
                            print(f"开始处理 {len(js_paths)} 个JS发现的403路径")
                            argument = Arguments(None, None, None, None)
                            argument.urls = js_urls
                            argument.dirs = js_paths
                            program = Program(argument.return_urls(), argument.return_dirs(), max_workers=20)
                            program.initialise()
                            
                    except Exception as e:
                        print(f"Error processing jsfind403list.txt: {str(e)}")
                
                pass403_qc()

        else:
            pass


def jsfind():
    import lib.JSFinder
    from lib.core.options import parse_options
    if (parse_options()['jsfind']) == None:
        pass
    else:
        jsf="".join(parse_options()['jsfind'])
        if jsf=='yes':
            print(Fore.GREEN + Style.BRIGHT+"Start JsFind!"+Style.RESET_ALL)
            url="".join(parse_options()['urls'])
            urls = lib.JSFinder.find_by_url(url)
            lib.JSFinder.giveresult(urls, url)
        else:
            pass

def ehole():
    import ehole.ehole
    from lib.core.options import parse_options
    if (parse_options()['zwsb']) == None:
        pass
    else:
        zwsb="".join(parse_options()['zwsb'])
        if zwsb=='yes':
            print(Fore.GREEN + Style.BRIGHT + "fingerprint identification!" + Style.RESET_ALL)
            ehole.ehole.start_ehole()
        else:
            pass


def hhh():
    open("403list.txt", 'w').close()
    open('jsfind403list.txt','w').close()

def swagger_scan():
    import lib.core.options
    from lib.core.data import options
    import swagger
    import argparse
    
    # 只调用一次 parse_options() 并存储结果
    parsed_options = lib.core.options.parse_options()
    
    # 检查 -swagger 参数是否为 yes
    if parsed_options.get('swagger') is None:
        return
    
    swagger_opt = "".join(parsed_options['swagger'])
    if swagger_opt.lower() != 'yes':
        return
    
    # 查找所有可能的 swagger 相关路径
    swagger_paths = []
    try:
        # 从扫描结果中读取所有找到的路径
        if os.path.exists('dir_file_path.txt'):
            with open('dir_file_path.txt', 'r') as f:
                report_path = f.read().strip()
                
            # 尝试读取报告文件中的路径
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    content = f.read()
                    # 检测 swagger 相关路径
                    swagger_patterns = ['swagger-ui', 'api-docs', 'swagger-resources', 'swagger.json', 'openapi.json']
                    for line in content.split('\n'):
                        # Skip empty lines
                        if not line.strip():
                            continue
                        
                        # Skip comment lines (start with #)
                        if line.strip().startswith('#'):
                            continue
                        
                        # Check if line contains any swagger pattern
                        if any(pattern in line.lower() for pattern in swagger_patterns):
                            try:
                                # Split the line by whitespace
                                parts = line.strip().split()
                                
                                # Check if the first part is a status code
                                if len(parts) >= 1:
                                    # Try to parse the status code
                                    try:
                                        status_code = int(parts[0])
                                        # Only include 200 status code paths
                                        if status_code != 200:
                                            print(f"Skipping non-200 status code path: {line.strip()}")
                                            continue
                                    except ValueError:
                                        # If first part is not a status code, skip this line
                                        print(f"Could not parse status code from line: {line.strip()}")
                                        continue
                                
                                # The full URL should be the third element or the last element
                                # depending on how the report is formatted
                                if len(parts) >= 3:
                                    # The URL could be the third part or possibly the last part
                                    # if there are spaces in the URL
                                    # Let's find the first part that starts with 'http'
                                    url_part = None
                                    for part in parts:
                                        if part.startswith('http'):
                                            url_part = part
                                            break
                                    
                                    if url_part:
                                        swagger_paths.append(url_part)
                                    else:
                                        # Fallback: use the last part as URL
                                        swagger_paths.append(parts[-1])
                                else:
                                    # Simple case: just use the entire line as URL
                                    swagger_paths.append(line.strip())
                            except Exception as e:
                                print(f"Error extracting URL from line: {line}. Error: {e}")
                                pass
    except Exception as e:
        print(f"Error reading swagger paths: {e}")
        pass
    
    # 如果找到了 swagger 路径，调用 swagger.py 进行扫描
    if swagger_paths:
        print(Fore.GREEN + Style.BRIGHT + f'Found {len(swagger_paths)} swagger related paths, starting swagger scan...' + Style.RESET_ALL)
        
        # 创建 swagger.py 需要的参数对象
        args = argparse.Namespace()
        args.target_url = None
        args.url_file = None
        args.debug = False
        args.force_domain = False
        args.custom_path_prefix = ''
        args.header_list = []
        # 获取 dirsearch 的 headers 并传递给 swagger 扫描
        args.custom_headers = parsed_options.get('headers', {})
        
        # 对每个找到的 swagger 路径进行扫描
        for swagger_url in swagger_paths:
            print(Fore.GREEN + f'Scanning swagger path: {swagger_url}' + Style.RESET_ALL)
            swagger.run(swagger_url, args)
            
        # 扫描完成后保存Excel文件
        try:
            base_name = "ScanReport"
            # 尝试从第一个swagger路径中提取域名作为文件名
            if swagger_paths:
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(swagger_paths[0]).netloc
                    safe_domain = re.sub(r'[.:\\/*?"<>|]', '_', domain)
                    base_name = safe_domain
                except Exception:
                    pass
            swagger.save_workbook(base_name)
        except Exception as e:
            print(f"Error saving swagger scan results to Excel: {e}")
    else:
        print(Fore.YELLOW + 'No swagger related paths found.' + Style.RESET_ALL)

def packer_fuzzer():
    import os
    import sys
    import subprocess
    from lib.core.options import parse_options
    
    # 检查 -p/--packer-fuzzer 参数
    if (parse_options()['packer_fuzzer']) == None:
        return
    
    packer_opt = "".join(parse_options()['packer_fuzzer'])
    if packer_opt.lower() != 'yes':
        return
    
    print(Fore.GREEN + Style.BRIGHT + "Start Packer-Fuzzer scan!" + Style.RESET_ALL)
    
    try:
        # 检查 bypass403_url.txt 文件是否存在并读取URL
        if os.path.exists('bypass403_url.txt'):
            with open('bypass403_url.txt', 'r') as f:
                url = f.read().strip()
                
            if url:
                print(f"Scanning URL: {url}")
                
                # 检查是否已经安装了 Packer-Fuzzer
                if not os.path.exists(os.path.join(os.getcwd(), 'Packer-Fuzzer')):
                    print(Fore.YELLOW + "Packer-Fuzzer not found. Cloning from GitHub..." + Style.RESET_ALL)
                    # 克隆 Packer-Fuzzer 仓库
                    subprocess.run([
                        'git', 'clone', 'https://github.com/rtcatc/Packer-Fuzzer.git'
                    ], check=True)
                    
                # 安装依赖
                if not os.path.exists(os.path.join(os.getcwd(), 'Packer-Fuzzer', 'venv')):
                    print(Fore.GREEN + "Installing Packer-Fuzzer dependencies..." + Style.RESET_ALL)
                    subprocess.run([
                        'python3', '-m', 'venv', 'venv'
                    ], cwd=os.path.join(os.getcwd(), 'Packer-Fuzzer'), check=True)
                    subprocess.run([
                        './venv/bin/pip', 'install', '-r', 'requirements.txt'
                    ], cwd=os.path.join(os.getcwd(), 'Packer-Fuzzer'), check=True)
                
                # 运行 Packer-Fuzzer 扫描
                print(Fore.GREEN + "Running Packer-Fuzzer scan..." + Style.RESET_ALL)
                result = subprocess.run([
                    './venv/bin/python', 'PackerFuzzer.py', '-u', url
                ], cwd=os.path.join(os.getcwd(), 'Packer-Fuzzer'), capture_output=True, text=True)
                
                # 查找生成的HTML报告
                import glob
                report_files = glob.glob(os.path.join(os.getcwd(), 'Packer-Fuzzer', 'reports', '*.html'))
                if report_files:
                    latest_report = max(report_files, key=os.path.getctime)
                    print(Fore.GREEN + "\nPacker-Fuzzer scan report found:" + Style.RESET_ALL)
                    print(f"Report path: {latest_report}")
                    print(Fore.CYAN + "\nYou can open this HTML report in your browser to view detailed scan results." + Style.RESET_ALL)
                    print(Fore.CYAN + "The report contains information about detected vulnerabilities, API endpoints, and other findings." + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "\nNo HTML report found. Check if Packer-Fuzzer completed successfully." + Style.RESET_ALL)
                    
                # 输出结果
                print(Fore.GREEN + "\nPacker-Fuzzer scan results:" + Style.RESET_ALL)
                print(result.stdout)
                
                if result.stderr:
                    pass
                    print(Fore.RED + "Packer-Fuzzer:" + Style.RESET_ALL)
                    print(result.stderr)
            else:
                print(Fore.RED + "No URL found in bypass403_url.txt" + Style.RESET_ALL)
        else:
            print(Fore.RED + "bypass403_url.txt not found" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error during Packer-Fuzzer scan: {str(e)}" + Style.RESET_ALL)


def main():

    hhh()

    from lib.core.options import parse_options

    options.update(parse_options())

    from lib.controller.controller import Controller

    Controller()

    jsfind()

    run_bypass403()

    ehole()
    
    packer_fuzzer()
    
    swagger_scan()



if __name__ == "__main__":
    q = queue.Queue()
    main()
