# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

from lib.Controller import Project
from lib.TestProxy import testProxy
from lib.common.banner import RandomBanner
from lib.common.cmdline import CommandLines
from lib.common.readConfig import ReadConfig
import signal
# 处理SIGINT信号 (CTRL+C)
def signal_handler(sig, frame):
    print('\n[!] 检测到中断信号，正在退出程序...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class Program():
    def __init__(self,options):
        self.options = options

    def check(self):
        url = self.options.url
        t = Project(url,self.options)
        t.parseStart()


if __name__ == '__main__':
    cmd = CommandLines().cmd()
    testProxy(cmd,1)
    try:
        PackerFuzzer = Program(cmd)
        PackerFuzzer.check()
    except KeyboardInterrupt:
        print('\n[!] 检测到中断信号，正在退出程序...')
    except Exception as e:
        print(f'[!] 程序执行出错: {str(e)}')
