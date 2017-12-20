#coding:utf-8
#author by Failymao

#搜索关键字
KEYWORD = 'apple'

#MongoDB服务器参数：连接地址，数据库名称，表名
MONGO_URL = '192.168.0.187'  
MONGO_DB = 'taobao'
MONGO_TABLE = 'taobao' + '_' + KEYWORD

#设置PantomJS不加载图片,开启缓存（默认不开）
SERVICE_ARGS = ['--load-images=false','--disk-cache=true'] 

