## dirsearch_bypass403


在安全测试时，安全测试人员信息收集中时可使用它进行目录枚举，枚举出来的403状态目录可尝试进行绕过，绕过403有可能获取管理员权限。不影响dirsearch原本功能使用

### 运行流程

dirsearch进行目录扫描--->将所有403状态的目录进行保存-->是否进行jsfind-->是(进行js爬取url和域名，将爬取到的url进行状态码识别如果是403状态则进行保存)-->进行403绕过

<img width="872" alt="image" src="https://user-images.githubusercontent.com/56328995/236988448-ffc37c6c-3446-4c99-aedf-7e27a08f2dff.png">

### 适用场景

安全测试人员在进行信息收集中时可使用它进行目录枚举发现隐藏目录，绕过403有可能获取管理员权限。

### 使用说明

默认不启用jsfind和403bypass

403bypass : -b yes

```
python dirsearch.py -u "http://www.xxx.com/" -b yes
```

jsfind ：-j yes

```
python dirsearch.py -u "http://www.xxx.com/" -j yes
```

jsfind和403bypass ： -b yes -j yes

```
python dirsearch.py -u "http://www.xxx.com/" -j yes -b yes
```

### 使用截图

<img width="1151" alt="image" src="https://user-images.githubusercontent.com/56328995/236655975-065acf6a-5fb6-4675-b9e4-fb958773140b.png">

<img width="854" alt="image" src="https://user-images.githubusercontent.com/56328995/236656001-1c2c0589-cbc4-42c4-87f4-6f73a5f95910.png">

<img width="550" alt="image" src="https://user-images.githubusercontent.com/56328995/236990089-dc7994ae-a00c-445b-aaa0-6df54572b821.png">


### 更新日志

#### 2023.5.7

增加页面长度一样的无效结果进行过滤输出

<img width="819" alt="image" src="https://user-images.githubusercontent.com/56328995/236655891-cae2798e-1ab6-49b0-b3db-0f59093a10e2.png">

#### 2023.5.9

是否进行jsfind查找js中的url，在网站的js文件中提取URl，排除（如png、gif）的URL，将403状态码的url进行403bypass

<img width="779" alt="image" src="https://user-images.githubusercontent.com/56328995/236984950-f704665e-997e-4b0a-bd1c-a35b58cd43e1.png">


### 参考优秀项目

dirsearch：https://github.com/maurosoria/dirsearch

403bypasser：https://github.com/yunemse48/403bypasser

JSFinder：https://github.com/Threezh1/JSFinder
