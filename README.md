## dirsearch_bypass403



### 运行流程

dirsearch进行目录扫描--->将所有403状态的目录进行保存-->进行403绕过

### 适用场景

安全测试人员在进行信息收集中时可使用它进行目录枚举发现隐藏目录，绕过403有可能获取管理员权限。

### 使用说明

默认不启用 参数 -b yes 启动403bypass

```
python dirsearch.py -u "http://www.xxx.com/" -b yes
```

###使用截图



### 2023.5.7

增加页面长度一样的无效结果进行过滤输出

<img width="819" alt="image" src="https://user-images.githubusercontent.com/56328995/236655891-cae2798e-1ab6-49b0-b3db-0f59093a10e2.png">



### 参考优秀项目

dirsearch：https://github.com/maurosoria/dirsearch

403bypasser：https://github.com/yunemse48/403bypasser
