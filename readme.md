##  财务工具

## 使用方法

### chrome驱动
- [chrome driver install](https://blog.csdn.net/n123456uo/article/details/91412740)
### python相关
- MacOs下重装
>- `brew unisntall python3`
>- 去[Taobao mirror](https://npm.taobao.org/mirrors/python/3.8.6/)下载最新的安装包
### python卸载
第一步：删除框架
```bash
sudo rm -rf /Library/Frameworks/Python.framework/Versions/2.7
```
第二步：删除应用目录
```bash
sudo rm -rf "/Applications/Python 2.7"
```
第三步：删除指向python的链接
```bash
cd /usr/local/bin/
ls -l /usr/local/bin | grep '/Library/Frameworks/Python.framework/Versions/2.7'                             # 查看链接
brew prune                  # 清除链接和目
```
## 其他要学习的python repo
https://github.com/tainzhi/CookiePool/blob/master/cookiepool/db.py

## 图形化PySimGUI
https://pysimplegui.readthedocs.io/en/latest/cookbook/
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Img_Viewer.py

## 打包工具 package to executable file
- 必须要在打包后生成exe的当前目录下放置如下目录（copy过去)
>- drivers: chrome driver
>- logs: 包含log的config文件

### 1 nuitka
- [nuikta官方readme怎么选择windows c compiler](https://github.com/Nuitka/Nuitka)
http://element-ui.cn/python/show-23924.aspx
https://zhuanlan.zhihu.com/p/133303836
https://zhuanlan.zhihu.com/p/141810934

### 2 pyinstaller

- download `pyinstaller` module
- in terminal window, type `pyinstaller -F main.py`, then the generated executable file is saved in `dist/`
- [pyinstaller不是交叉编译软件, 可以跨平台, 但是要在不同平台分别打包; 对运行性能没有直接影响](https://gitchat.csdn.net/activity/5c8f101aa7494e3e31a04743)
- 为了减小打包体积, 只import需要的module
- 打包的程序闪退，解决办法**从terminal执行exe程序， 输出错误信息到terminal
- [pyinstaller打包后资源路径怎么选择](https://blog.csdn.net/qq_31801903/article/details/81666124)
- parameter
>- `-F`, generated single zip executable file; without `-F`, 生成一堆文件， 但运行速度快
>- `-w`, 禁止弹出控制台窗口, 生成gui程序
>- `--uac-admin`, `-m`, manifest File
>- `-i <icon File`, icon
```bash
pyinstaller -F -w -i account.ico -n "财务助手" main.py
```

## pipenv
- 改变source， 根目录下的`Pipfile`url为, 同时更改name, ide会自动弹出Notification提醒**pipenv update**
- 优点: 跨平台支持良好(不同平台不产生多余配置文件), 不产生env目录, 自动管理更新下载依赖包 
```
https://mirrors.aliyun.com/pypi/simple/
```

## 包错误
- [安装最新版本的上一个版本](https://blog.csdn.net/HsinglukLiu/article/details/109555299)


## Todo
- 验证最终的结果，是否全部抓取
- 抓取时，被网站反爬虫，怎么重新从剩余未抓取的重新抓取，而不是全部从头抓取
- selenium 使用proxy，我的服务器搭建一个proxy_pool库(git hub上搜索合适 的)
- docker,docker-comse的用法 https://github.com/notfresh/shorturl_service
- [添加执行icon和管理员权限盾牌](https://blog.csdn.net/laiyaoditude/article/details/85278037)
- nuitka打包成exe
- python async
- 架构图

## python学习
- [python class](https://www.runoob.com/python3/python3-class.html): Selenium支持跨平台(win10/mac)
- [python multi thread](https://www.runoob.com/python3/python3-multithreading.html)
- [python 4种截屏方法](https://www.jb51.net/article/168609.htm)
- [selenium反爬虫](https://blog.csdn.net/weixin_44685869/article/details/105602629?utm_medium=distribute.pc_relevant.none-task-blog-title-3&spm=1001.2101.3001.4242)
- [python selenium指定元素截长图](https://cloud.tencent.com/developer/article/1406656)
- [python string format](https://www.runoob.com/python/att-string-format.html)
```python
>>>"{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
'hello world'
 
>>> "{0} {1}".format("hello", "world")  # 设置指定位置
'hello world'
 
>>> "{1} {0} {1}".format("hello", "world")  # 设置指定位置
'world hello world'
print("网站名：{name}, 地址 {url}".format(name="菜鸟教程", url="www.runoob.com"))
```

## pickle保存dict/list
```python
mydict = {"1": 10, "3": 30}
with open("./data/medFile/test.pickle", "wb") as fp:   #Pickling
    pickle.dump(mydict, fp, protocol = pickle.HIGHEST_PROTOCOL)      
with open("./data/medFile/test.pickle", "rb") as fp:   #Pickling
    mydict = pickle.load(fp)     
mydict
```

## selenium多线程
- 对同一个网站多线程爬取，会很容易被网站检测出爬虫行为，而被禁止
- css selecotr多个class选取
```html
<div class="search header" name="hello" search="ok">
   <div class="header" name="world>
   </div>
</div>
```
- 那么css class selector为`.search.header`, **中间没有空格**,匹配外层element
- css selector用法为`".search,[search='ok']"`,匹配外层element
- css属性selector为`[name=hello]`
- css class selector为`.search .header`(**中间有空格**), 匹配到的是内层element


## 有用的库
- selenium 控制chrome，也可跨平台截全屏图
- cpca 可以获取标准化的省市区地址
- pillow 图片截取crop
- threading 多线程，线程库
- [logging logger](https://www.cnblogs.com/qianyuliang/p/7234217.html)
- shelve 简单的持久化到硬盘，dict类型