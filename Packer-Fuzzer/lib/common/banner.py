# !/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
from lib.common.utils import Utils
from lib.common.cmdline import CommandLines


Version = 'Packer Fuzzer v1.4.15'
red = '\033[25;31m'
green = '\033[25;32m'
yellow = '\033[25;33m'
blue = '\033[25;34m'
Fuchsia = '\033[25;35m'
cyan = '\033[25;36m'
end = '\033[0m'
colors = [red,green,yellow,blue,Fuchsia,cyan]

Banner1 = """{}
 _______________
< Packer Fuzzer >
 ---------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\\
                ||----w |
                ||     ||
           {}
{}
""".format(random.choice(colors),Version,end)

Banner2 = """{}
 _______________
< Packer Fuzzer >
 ---------------
   \\
    \\
        .--.
       |o_o |
       |:_/ |
      //   \ \\
     (|     | )
    /'\_   _/`\\
    \___)=(___/
       {}
 {}
""".format(random.choice(colors),Version,end)

Banner3 = '''{}
 _______________
< Packer Fuzzer >
 ---------------
    \\
     \\
                                   .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$#
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$*
      ^$$$B  $$$$\     $$$$$$$$$$$$   d$$R"
        "*$bd$$$$      '*$$$$$$$$$$$o+#"
             """"          """""""
             {}
{}
'''.format(Fuchsia,Version,end)

Banner7 = ""

def RandomBanner():
    # BannerList = [Banner1,Banner2,Banner3,Banner7]
    if CommandLines().cmd().silent == None:
        print(Banner7)
        print(Utils().getMyWord("{xhlj}") + "\n")


RandomBanner()
