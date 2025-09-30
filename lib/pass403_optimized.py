import requests
import validators
import os
import tldextract
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from colorama import init, Fore, Style
from pyfiglet import Figlet
from requests.packages import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

urllib3.disable_warnings()
init()

class OptimizedArguments():
    def __init__(self, url, urllist, dir, dirlist):
        self.url = url
        self.urllist = urllist
        self.dir = dir
        self.dirlist = dirlist
        self.urls = []
        self.dirs = []

        self.checkURL()
        self.checkDir()

    def return_urls(self):
        return self.urls

    def return_dirs(self):
        return self.dirs

    def checkURL(self):
        if self.url:
            if not validators.url(self.url):
                sys.exit()
            if self.url.endswith("/"):
                self.url = self.url.rstrip("/")
            self.urls.append(self.url)
        elif self.urllist:
            if not os.path.exists(self.urllist):
                sys.exit()
            with open(self.urllist, 'r') as file:
                temp = file.readlines()
            for x in temp:
                self.urls.append(x.strip())
        else:
            sys.exit()

    def checkDir(self):
        if self.dir:
            if not self.dir.startswith("/"):
                self.dir = "/" + self.dir
            if self.dir.endswith("/") and self.dir != "/":
                self.dir = self.dir.rstrip("/")
            self.dirs.append(self.dir)
        elif self.dirlist:
            if not os.path.exists(self.dirlist):
                sys.exit()
            with open(self.dirlist, 'r') as file:
                temp = file.readlines()
            for x in temp:
                self.dirs.append(x.strip())
        else:
            self.dir = "/"

class OptimizedPathRepository():
    def __init__(self, path):
        self.path = path
        self.newPaths = []
        self.newHeaders = []
        self.rewriteHeaders = []
        self.createNewPaths()
        self.createNewHeaders()

    def createNewPaths(self):
        self.newPaths.append(self.path)
        
        pairs = [["/", "//"], ["/.", "/./"]]
        leadings = ["/%2e"]
        trailings = ["/", "/*/", "/*", "..;/", "/..;/", "%20", "%09", "%00",
                    ".json", ".css", ".html", "?", "??", "???",
                    "?testparam", "#", "#test", "/."]

        for pair in pairs:
            self.newPaths.append(pair[0] + self.path + pair[1])
        for leading in leadings:
            self.newPaths.append(leading + self.path)
        for trailing in trailings:
            self.newPaths.append(self.path + trailing)

    def createNewHeaders(self):
        headers_overwrite = ["X-Original-URL", "X-Rewrite-URL"]
        headers = ["X-Custom-IP-Authorization", "X-Forwarded-For",
                  "X-Forward-For", "X-Remote-IP", "X-Originating-IP",
                  "X-Remote-Addr", "X-Client-IP", "X-Real-IP"]
        values = ["localhost", "localhost:80", "localhost:443",
                 "127.0.0.1", "127.0.0.1:80", "127.0.0.1:443",
                 "2130706433", "0x7F000001", "0177.0000.0000.0001",
                 "0", "127.1", "10.0.0.0", "10.0.0.1", "172.16.0.0",
                 "172.16.0.1", "192.168.1.0", "192.168.1.1"]

        for header in headers:
            for value in values:
                self.newHeaders.append({header: value})
        for element in headers_overwrite:
            self.rewriteHeaders.append({element: self.path})

class OptimizedQuery():
    def __init__(self, url, dir, dirObject, session=None, timeout=5, max_retries=2):
        self.url = url
        self.dir = dir
        self.dirObject = dirObject
        self.domain = tldextract.extract(self.url).domain
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 创建优化的session
        self.session = session or self._create_optimized_session()
        
        # 结果存储
        self.results = []
        self.lock = threading.Lock()

    def _create_optimized_session(self):
        """创建优化的session配置"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # 配置适配器
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,  # 连接池大小
            pool_maxsize=100,     # 最大连接数
            pool_block=False
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 设置默认headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        })
        
        return session

    def checkStatusCode(self, status_code):
        if status_code == 200 or status_code == 201:
            return Fore.GREEN + Style.BRIGHT
        elif status_code == 301 or status_code == 302:
            return Fore.BLUE + Style.BRIGHT
        elif status_code == 403 or status_code == 404:
            return Fore.MAGENTA + Style.BRIGHT
        elif status_code == 500:
            return Fore.RED + Style.BRIGHT
        else:
            return Fore.WHITE + Style.BRIGHT

    def send_request(self, method, url, **kwargs):
        """优化的请求方法"""
        try:
            response = self.session.request(
                method, url, 
                timeout=self.timeout, 
                verify=False, 
                **kwargs
            )
            return response
        except requests.RequestException:
            return None

    def process_path(self, path, method='GET', headers=None):
        """处理单个路径"""
        try:
            r = self.send_request(method, self.url + path, headers=headers)
            if r is None:
                return None

            colour = self.checkStatusCode(r.status_code)
            reset = Style.RESET_ALL
            line_width = 70

            target_address = f"{method} --> {self.url}{path}"
            info = f"STATUS: {colour}{r.status_code}{reset}\tSIZE: {len(r.content)}"
            info_pure = f"STATUS: {r.status_code}\tSIZE: {len(r.content)}"
            remaining = line_width - len(target_address)

            result = {
                'target': target_address,
                'info': info,
                'info_pure': info_pure,
                'remaining': remaining,
                'status_code': r.status_code,
                'content_length': len(r.content),
                'headers': headers
            }

            # 只显示非403状态码
            if r.status_code != 403:
                print(target_address + " " * remaining + info + '\n', end='')
                if headers:
                    print(f"Header= {headers}" + '\n', end='')

            return result
        except Exception:
            return None

    def manipulateRequest(self):
        """优化的请求处理"""
        # POST请求
        post_result = self.process_path(self.dir, 'POST')
        if post_result:
            self.results.append(post_result)

        # 并发处理路径变异
        self._process_paths_concurrently()

        # 并发处理header变异
        self._process_headers_concurrently()

    def _process_paths_concurrently(self):
        """并发处理路径变异"""
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for path in self.dirObject.newPaths:
                future = executor.submit(self.process_path, path)
                futures.append(future)

            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.results.append(result)

    def _process_headers_concurrently(self):
        """并发处理header变异"""
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            # 处理普通headers
            for header in self.dirObject.newHeaders:
                future = executor.submit(self.process_path, self.dir, 'GET', header)
                futures.append(future)

            # 处理重写headers
            for header in self.dirObject.rewriteHeaders:
                future = executor.submit(self.process_path, '', 'GET', header)
                futures.append(future)

            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.results.append(result)

    def writeToFile(self):
        """批量写入文件"""
        if not self.results:
            return

        filename = f"{self.domain}.txt"
        with open(filename, "a") as file:
            for result in self.results:
                line = result['target'] + " " * result['remaining'] + result['info_pure']
                if result['headers']:
                    line += f"---Header= {result['headers']}"
                file.write(line + "\n")

class OptimizedProgram():
    def __init__(self, urllist, dirlist, max_workers=20):
        self.urllist = urllist
        self.dirlist = dirlist
        self.max_workers = max_workers
        # 创建共享的session池
        self.session_pool = Queue()
        for _ in range(min(10, len(urllist))):
            self.session_pool.put(self._create_optimized_session())

    def _create_optimized_session(self):
        """创建优化的session"""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=20,
            pool_maxsize=100,
            pool_block=False
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        })
        
        return session

    def _get_session(self):
        """从池中获取session"""
        try:
            return self.session_pool.get_nowait()
        except:
            return self._create_optimized_session()

    def _return_session(self, session):
        """归还session到池中"""
        try:
            self.session_pool.put_nowait(session)
        except:
            pass

    def process_url_dir_combination(self, url, dir_path):
        """处理单个URL和路径的组合"""
        session = self._get_session()
        try:
            if dir_path != "/":
                dir_objname = dir_path.lstrip("/")
            else:
                dir_objname = "_rootPath"
            
            dir_obj = OptimizedPathRepository(dir_path)
            query = OptimizedQuery(url, dir_path, dir_obj, session=session)
            query.manipulateRequest()
            query.writeToFile()
        finally:
            self._return_session(session)

    def initialise(self):
        """优化的初始化方法"""
        print(f"开始处理 {len(self.urllist)} 个URL和 {len(self.dirlist)} 个路径")
        print(f"使用 {self.max_workers} 个并发工作线程")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            # 为每个URL和路径组合创建任务
            for url in self.urllist:
                for dir_path in self.dirlist:
                    future = executor.submit(self.process_url_dir_combination, url, dir_path)
                    futures.append(future)
            
            # 等待所有任务完成
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                try:
                    future.result()
                    completed += 1
                    if completed % 10 == 0:
                        print(f"进度: {completed}/{total} ({completed/total*100:.1f}%)")
                except Exception as e:
                    print(f"任务执行出错: {e}")
        
        end_time = time.time()
        print(f"处理完成! 总耗时: {end_time - start_time:.2f} 秒")
        print(f"平均每个任务耗时: {(end_time - start_time) / total:.2f} 秒")
