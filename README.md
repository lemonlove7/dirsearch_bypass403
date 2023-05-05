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
