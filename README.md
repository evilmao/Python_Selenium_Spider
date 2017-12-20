# Python_Selenium_Spider
结合selenium+PantomJs/Chrome爬取淘宝搜索相关宝贝信息



## Requiretments

Running Environment(运行环境)

- Python 3.5+ 
- Linux(测试环境使用的是centos7)/Windows/MAC OS
- 工具使用： Eclipse / Pycharm 

## skill tree

需要简单学习一些前端的知识：

- HTML（网页结构，各种标签）
- Xpath（基本的定位要了解，轴的内容可以在有一定基础之后再学）
- CSS（简单了解）
- JavaScript（简单了解）
- Firebug（开发者工具）的使用（这个经常会用到，必须熟悉，可在selenium学习中逐渐深入）
- 网络基础知识

## library(库)

* pip install  pymongo (python操作MongoDB数据库包)
* pip install selenium
* pip install  pyquery

## Third-part Tools

 为使用selenium 模拟浏览器功能需要提前安装相关浏览器的 驱动器

> 这里用一些主流的浏览器即可 Chrome ,Firefox ,Edge
>
> 此外介绍一款无图形界面的浏览器 PhantomJS,开发神器
>
> 

具体下载地址，自行google一下！

***这里需要提示一下，所有的driver下载完毕后，务必加入到python相应版本的目录下，否则调用时，会报错（windows下，linux具体目录根据版本不同请自行google）***

如下图（windows 10）

![](http://ww1.sinaimg.cn/large/8599e4cfly1fmnekpum10j20kn06h74n.jpg)

## Problem analysis

> 详细分析过程参考 代码注释部分
>
> * 想要熟练使用selenium 爬虫，需对前端知识和selenium各种相关方法有一定的知识积累



## Update

 程序比较粗糙，重在理解selenium爬取复杂网站的优势，具体优化方案很多！后期有时间再捯饬



