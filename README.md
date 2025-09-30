## dirsearch_bypass403


在安全测试时，安全测试人员信息收集中时可使用它进行目录枚举，目录进行指纹识别，枚举出来的403状态目录可尝试进行绕过，绕过403有可能获取管理员权限。不影响dirsearch原本功能使用

### 运行流程

dirsearch进行目录扫描--->将所有403状态的目录进行保存-->是否进行jsfind-->是(进行js爬取url和域名，将爬取到的url进行状态码识别如果是403状态则进行保存)-->进行403绕过-->目录进行指纹识别

<img width="848" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/db2d9226-4b0f-4d37-9501-6c24eef8c7b2">

### 视频演示

https://www.bilibili.com/video/BV1J14y1k7o3/

### python环境
建议使用python<3.10，，高版本可能存在兼容问题
测试环境python=3.8.20

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

单独对指定目录进行bypass

```
python single_403pass.py -u "http://www.xxx.com/" -p "/index.php" # -p 指定路径
```

对扫描出来的目录进行指纹识别(结果会自动保存在reports目录下的.josn文件中)

```
python dirsearch.py -u "http://www.xxx.com/" -z yes
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

#### 2023.5.11
优化原版403bypasser，单独对某一指定路径进行403bypass

昨天同事在使用时遇到问题：发现一个403页面，如果运行dirsearch则会目录扫描后再403bypass

single_403pass.py 单独对一个url指定路径进行403bypass

```
python single_403pass.py -u "http://www.xxx.com/" -p "/index.php" # -p 指定路径
```

<img width="965" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/6698201c-734d-411a-92ba-379da6f4c5f0">

#### 2023.5.12

对目录进行指纹识别(结果会自动保存在reports目录下的.josn文件中)

```
python dirsearch.py -u "http://www.xxx.com/" -z yes
```

<img width="1046" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/2a6d5ad8-81cd-4408-b6c9-860d2e153ad9">

#### 2023.5.22

对404状态码和0B数据进行过滤不进行指纹识别

#### 2023.9.1
实验环境：https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented

优化403bypass：与首页大小进行判断 如果size相同则表示绕过失败

增加了一点403bypass绕过方式

<img width="1245" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/b9075d68-85f7-439b-886d-3748978b9962">
<img width="1052" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/933ac6e9-13a8-4a66-8ac2-52192c83b08a">
<img width="1053" alt="image" src="https://github.com/lemonlove7/dirsearch_bypass403/assets/56328995/5b2185c6-6680-4225-ab64-de8cde667791">

#### 2025.9.30

1.403bypass检测优化，以及扫描速度提升,根据电脑自身cpu调整线程；

2.修复若干问题：在设置代理时无法扫描：[#12](https://github.com/lemonlove7/dirsearch_bypass403/issues/12),最新版使用ehole功能时报错：[#11](https://github.com/lemonlove7/dirsearch_bypass403/issues/11),[#10](https://github.com/lemonlove7/dirsearch_bypass403/issues/10),逻辑问题：[#4](https://github.com/lemonlove7/dirsearch_bypass403/issues/4)

3.增加实用功能：

3.1 融合Packer-Fuzzer,可查看：[#9](https://github.com/lemonlove7/dirsearch_bypass403/issues/9)

如果提示模块已经安装还提示未安装，在/Packer-Fuzzer目录下将venv删除重新运行即可

```
python dirsearch.py -u "http://www.xxx.com/" -p yes
```
<img width="882" height="196" alt="image" src="https://github.com/user-attachments/assets/51853d09-7428-4349-98fb-2343ecfb8b1a" />

<img width="1063" height="802" alt="image" src="https://github.com/user-attachments/assets/a48a78af-0022-45fc-a9a3-d829eb23c466" />

3.2 增加对swagger的未授权扫描

如果在目录扫描中出现swagger的路径并且未200，size大小不为0，则在目录扫描后会进行swagger未授权测试

```
python dirsearch.py -u "http://www.xxx.com/" --swagger yes
```

<img width="1054" height="447" alt="image" src="https://github.com/user-attachments/assets/18617837-b0d9-44da-aced-c73e1e68ca94" />
<img width="1401" height="560" alt="image" src="https://github.com/user-attachments/assets/e947b85e-b304-4d17-985e-97bfe9437aa2" />



### 参考优秀项目

> dirsearch：https://github.com/maurosoria/dirsearch

> 403bypasser：https://github.com/yunemse48/403bypasser

> JSFinder：https://github.com/Threezh1/JSFinder

> EHole：https://github.com/EdgeSecurityTeam/EHole

>Packer-Fuzzer:https://github.com/rtcatc/Packer-Fuzzer 

### Star历史

![Star History Chart](https://api.star-history.com/svg?repos=lemonlove7/dirsearch_bypass403&type=Date)
