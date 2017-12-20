#coding:utf-8
#author by Failymao
'''
    分析
    - 搜索关键字，利用Selenium驱动浏览器搜索，得到查询后的商品列表
    - 分析页码并翻页，得到商品页码数，得到后续页面的商品列表
    - 分析提取商品内容，利用PyQuery分析源码，解析得到商品列表
    - 存储至MongoDB
'''
import re
import pymongo
from config import *
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException                  #导入等待超时模块
from pyquery import PyQuery as pq


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

#driver = webdriver.Chrome()
driver =  webdriver.PhantomJS(service_args=SERVICE_ARGS)                        #使用PhantomJS模块，模拟无界面浏览器，使加载速度更快，参数为一个列表[不加载图片，开启缓存]
wait = WebDriverWait(driver, 10)                                                #设置浏览器等待时间，便于页面元素全部加载
driver.set_window_size(1440, 900)                                               #设置窗口大小

def search():
    '''进入淘宝主页，搜索页面'''
    print ('正在搜索')
    try:
        driver.get('https://www.taobao.com')                                     #浏览器打开淘宝首页
        element  = wait.until(EC.presence_of_element_located(                    #通过wait.until()方法，确认直到指定的元素加载完毕;EC用来设定预先设定的条件
                                (By.CSS_SELECTOR, '#q'))                         #presence_of_element_located方法用来定义一个元素的位置
                              )                                                  #By.CSS_SELECTOR使用css选择器通过css属性，定义属性 --这里的'#q’通过开发者工具（f12），确定输入框css属性
        button = wait.until(EC.element_to_be_clickable(                          #element_to_be_clickable定义按键操作方法
                                (By.CSS_SELECTOR, 
                                '#J_TSearchForm > div.search-button > button'    #通过css_selector定位搜索框的CSS属性位置
                                )
                                                       )
                            )
        element.send_keys(KEYWORD)                                               #通过send_kesy方法将搜索的关键字发送至搜索框
        button.click()                                                           #通过click方法用来进行搜索按键 点击的确认操作
        total = wait.until(EC.presence_of_element_located(                       #保证首页所有搜索到的商品元素加载完毕
                                (By.CSS_SELECTOR, 
                                 '#mainsrp-pager > div > div > div > div.total') #同理用css_selector方法，定位到搜索到的总页数
                                                          )
                            )
        get_prodects_detail()                                                    #调用提取第一页所有商品详情的函数
        return total.text                                                        #返回搜到商品的页面数                                         
    except TimeoutException:                                                     #出现超时错误
        return search(KEYWORD)                                                   #继续调用函数
    
def next_page(page_number):
    '''翻页操作函数'''
    print ('正在加载{}页'.format(page_number))
    try:
        element  = wait.until(EC.presence_of_element_located(                    #同样通过wait,until方法设置加载完成条件后执行后续操作
                                    (By.CSS_SELECTOR,                            #定位到页面输入框位置
                                     '#mainsrp-pager > div > div > div > div.form > input'))
                              )
        button = wait.until(EC.element_to_be_clickable(                          #定位到页面输入框后的确定按键
                                    (By.CSS_SELECTOR,
                                    '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
                            )
        element.clear()                                                          #在输入跳转的页面数字前需要情况输入框的内容
        element.send_keys(page_number)                                           #传入指定需要访问的页面 数
        button.click()                                                           #click()点击确定跳转到页面
        wait.until(EC.text_to_be_present_in_element(                             #text_to_be_present_in_element()方法来判断某文本是否在该元素的文本内容中
                                    (By.CSS_SELECTOR,                            #定位当前页面页码CSS元素的位置，与指定跳转的页面页码是否匹配
                                    '#mainsrp-pager > div > div > div > ul > li.item.active > span'
                                    ),str(page_number)                           #指定的输入需要访问的页码数
                                    )               
                   )
        get_prodects_detail()                                                   #调用提取当前页面所有商品详情的函数
    except TimeoutException:                                                    #出现超时异常，继续加载当前页面
        next_page(page_number)
        
def get_prodects_detail():
    '''获取当前页面所有商品信息详情'''
    wait.until(EC.presence_of_element_located(                                  #分析页面,等待页面所选商品所有元素加载完毕
                                 (By.CSS_SELECTOR,
                                 '#mainsrp-itemlist .items .item')              #注意元素分层关心，准确找到每个商品元素的CSS_SELECTOR
                                 )
               )
    html = driver.page_source                                                   #获取当前页面的源码信息，为list数据类型
    doc = pq(html)                                                              #通过pyquery.PyQuery（）方法获取当前页面（从源码中）获得所有的元素
    items = doc('#mainsrp-itemlist .items .item').items()                       #定位每个商品的元素快，提取出所有满足的条目
    for item in items:                                                          #遍历每个商品的元素区域-pyquery对象，从中取出想提取的信息，
        product = {
            'image':item.find('.pic .img').attr('src'),                         #通过pyquery.find()通过内部css_to_xpathy的css定位方法找到想提取的css属性
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
            }
        #print(product)
        save_to_mongo(product)                                                  #将提取的商品信息以字典（json格式）插入到mongoDB数据库中

def save_to_mongo(result):
    '''将数据保存到MongoDB，参数为插入到数据库的信息'''
    try:
        if db[MONGO_TABLE].insert(result):                                      #insert方式插入到MongoDB
            print ('存储到数据库成功', result)
    except Exception:
        print ('保存失败', result)
      
def main():
    '''主函数'''
    try:                                                                        #try...异常判断
        total = search()                                                 
        total_pages = int(re.compile('(\d+)').search(total).group(1))           #正则表达式用来分离出搜索到商品页码数
        for i in range(2, total_pages+1):
            next_page(i)
    except Exception:
        print ('出错啦!')   
    finally:                                                                    #finally确保无论是否执行成功，最终都会关闭浏览器
        driver.quit()


#-----------------分割线——————————————————
if __name__ == "__main__":
    main()
    
    
    
    