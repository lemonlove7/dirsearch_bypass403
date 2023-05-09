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

from colorama import init, Fore, Style

from lib.pass403 import Arguments,Program
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
    with open('bypass403_url.txt') as f:
        bypass403_url=f.read()
    while not q.empty():
        path_403=q.get()
        try:
            argument = Arguments(bypass403_url, None, path_403, None)
            program = Program(argument.return_urls(), argument.return_dirs())
            program.initialise()
        except:
            pass


def run_bypass403():
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
                with open('403list.txt',) as f1:
                    list_403=f1.readlines()
                for path_403 in list_403:
                    path_403=path_403.replace('\n','').replace('\r','')
                    q.put(path_403)
                thread_list = []
                for i in range(20):
                    t = threading.Thread(target=bypass)
                    thread_list.append(t)
                for t in thread_list:
                    t.setDaemon(True)
                    t.start()
                for t in thread_list:
                    t.join()

                if size_js == 0:
                    pass
                else:
                    try:
                        with open('jsfind403list.txt') as js1:
                            jsf=js1.readlines()
                        def process_ff(ff):
                            ff = ff.replace('\n', '').replace('\r', '')
                            num_slashes = ff.count('/')
                            if num_slashes == 2:
                                ff = ff + '/'
                            split_url = ff.split("/")
                            js_url = "/".join(split_url[:3])
                            js_path = split_url[3]
                            if js_path == '':
                                js_path = '/'
                            argument = Arguments(js_url, None, js_path, None)
                            program = Program(argument.return_urls(), argument.return_dirs())
                            program.initialise()

                        def js_403():
                            with ThreadPoolExecutor() as executor:
                                executor.map(process_ff, jsf)
                        js_403()
                    except:
                        pass
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


def hhh():
    open("403list.txt", 'w').close()
    open('jsfind403list.txt','w').close()


def main():

    hhh()

    from lib.core.options import parse_options

    options.update(parse_options())

    from lib.controller.controller import Controller

    Controller()

    jsfind()

    run_bypass403()




if __name__ == "__main__":
    q = queue.Queue()
    main()
