from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import itchat
import re
import matplotlib.pyplot as plt
import os
import numpy as np


# 加入邮件通知按钮


# 文件信息读取
def TxtReading():
    user={}
    a=0
    file = open("config.txt", "r+")
    while 1:

        line = file.readline()
        if not line:
            break
        print(line)
        if a == 0:
            user['ID'] = line[3:]
        if a == 1:
            user['PassWord'] = line[9:]
        if a == 2:
            user['Payment_password'] = line[17:]
        if a == 3:
            user['Game'] = line[5:]
        if a == 4:
            user['Product']=line[8:]
        a=a+1
    return user



# 判断元素存在方法
# 缺点：当元素不存在时判断时间过长
def exist(web, find):
    try:
        if web.find_element_by_xpath(find):
            return 1
    except:
        return 2


# 声明浏览器 返回浏览器对象
def Browser():
    chrome_options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--window-size=1280,800")
    # chrome_options.binary_location = "C:\Program Files (x86)\Chrome\Application\chromedriver.exe"
    # 声明浏览器
    # web = webdriver.Chrome(chrome_options=chrome_options)

    web = webdriver.Chrome("H:\Program Files (x86)\Chrome\Application\chromedriver.exe")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    web.set_window_size(1280, 800)
    return web


# 登陆   user:用户名    password：密码
def Log_in(web, user, password):
    web.get("https://www.igxe.cn")
    # 点击登陆
    web.find_element_by_xpath("//*[@id=\"header\"]/div[1]/div/div/div[2]/ul/li[1]/a").send_keys(Keys.ENTER)
    # 输入账号密码
    web.find_element_by_xpath("//*[@id=\"username\"]").send_keys(str(user))
    web.find_element_by_xpath("//*[@id=\"password\"]").send_keys(str(password))
    # 点击登陆
    # web.find_element_by_xpath("//*[@id=\"login-form\"]/div[5]/input").send_keys(Keys.ENTER)
    return web




# Game 购买的那个游戏的专区
# Article 扫物品的名称
# Price 物品需要的价格
# Passwd 交易密码
def Scan(web,Game,Article,Price,Passwd):

    # 转向pubg专区
    Game = "https://www.igxe.cn/" + str(Game)
    web.get(Game)
    # 查询特定衣服

    web.find_element_by_xpath("//*[@id=\"js-search-key\"]").send_keys(Article)
    # 点击搜索
    web.find_element_by_xpath("//*[@id=\"js-search-key\"]").send_keys(Keys.ENTER)
    # 点击搜索出的第一个内容
    web.find_element_by_xpath("//*[@id=\"center\"]/div[2]/div/div[3]/ul/li/div[1]/a").send_keys(Keys.ENTER)
    web.implicitly_wait(10)
    url = web.current_url
    pay(web=web,url=url,Price=Price,Passwd=Passwd)

def pay(web,url,Price,Passwd):
    web.get(url)
    time.sleep(0.3)
    # 点击批量购买
    web.find_element_by_xpath("//*[@id=\"js-btn-tradeBuy\"]").click()
    # 找到弹出的批量框
    web.find_element_by_xpath("//*[@id=\"layui-layer1\"]")
    # 清空价格框
    web.find_element_by_xpath("//*[@id=\"js-money-end\"]").clear()
    # 点击购买的价格
    web.find_element_by_xpath("//*[@id=\"js-money-end\"]").send_keys(Price)

    while True:
        # 点击查询
        print("进入购物车5")
        web.find_element_by_xpath("//*[@id=\"js-pop-weaponKey\"]/div[1]/div[2]/dl[3]/dd/div/input").click()
        # 强制暂停 等待刷新的页面
        time.sleep(0.4)
        web.implicitly_wait(10)
        a = web.find_element_by_xpath("//*[@id=\"js-size\"]").text
        # 判断物品
        print(a)
        if int(a) == None:
            continue
        if int(a) > 0:
            try:
                print("进入购物车")
                # 点击购物车
                web.find_element_by_xpath("//*[@id=\"js-add-standard-cart\"]").click()
                # 输入支付密码
                Available_Balance = web.find_element_by_xpath(
                    "//*[@id=\"pay_order_form\"]/div[2]/div[2]/ul/li/label/p[2]/b").text.strip("￥")
                Available_Car = web.find_element_by_xpath('//*[@id="span_pay_money"]').text
                print(Available_Balance + "   " + Available_Car)
                print("进入购物车1")
                # if web.find_element_by_xpath("//*[@id=\"pay_order\"]").is_displayed():
                #     print("!!!!!")
                #     web.find_element_by_xpath("//*[@id=\"js-shopping-cart\"]/div/a").click()
                #     web.find_element_by_xpath("//*[@id=\"pay_order_form\"]/div[4]/div[2]/span/a[1]").send_keys(
                #         Keys.ENTER)
                #     pass
                if Available_Balance > Available_Car:
                    print("进入！！！")
                    web.find_element_by_xpath("//*[@id=\"pay-pwd\"]").send_keys(Passwd)
                    web.find_element_by_xpath("//*[@id=\"pay_order\"]").send_keys(Keys.ENTER)
                    # web.find_element_by_xpath("//*[@id=\"layui-layer2\"]")
                    web.find_element_by_link_text("确定").click()
                    web.find_element_by_link_text("确定").click()
                    itchat.send_msg('扫号成功！')
                    pay(web=web, url=url, Price=Price, Passwd=Passwd)
                elif Available_Balance < Available_Car:
                    print("余额不足,请充值！")
                    itchat.send_msg('余额不足,请充值！')
                    web.quit()
                    break
                print("进入购物车2")
            # web.find_element_by_xpath("//*[@id=\"layui-layer1\"]/div[3]/a[1]").click()
            except:
                # 判断失效物品
                print("进入购物车3")
                if exist(web, "//*[@id=\"js-shopping-cart\"]/div/a") == 1:
                    print("123")
                    web.find_element_by_xpath("//*[@id=\"js-shopping-cart\"]/div/a").click()
                    web.implicitly_wait(3)
                # 判断价格
                if exist(web, "//*[@id=\"pay_order_form\"]/div[4]/div[2]/span") == 1:
                    web.find_element_by_xpath("//*[@id=\"pay_order_form\"]/div[4]/div[2]/span")
                    print("321")
                    web.find_element_by_link_text("确认").send_keys(Keys.ENTER)
                    web.find_element_by_xpath("//*[@id=\"pay_order_form\"]/div[4]/div[2]/span/a[1]").send_keys(
                        Keys.ENTER)
                    print("进入购物车4")
                web.find_element_by_xpath("//*[@id=\"pay-pwd\"]").send_keys(Passwd)
                web.find_element_by_xpath("//*[@id=\"pay_order\"]").send_keys(Keys.ENTER)
                # web.find_element_by_xpath("//*[@id=\"layui-layer2\"]")
                web.find_element_by_link_text("确定").click()
                web.find_element_by_link_text("确定").click()
                pay(web=web, url=url, Price=Price, Passwd=Passwd)
                time.sleep(3)
        web.quit()
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # 返回同样的文本消息
    print(msg['Text'])

if __name__ == "__main__":
    itchat.auto_login(hotReload=True)
    #itchat.send('text', toUserName='filehelper')
    # print("123")
    # itchat.run()
    user = TxtReading()
    id = user['ID']
    password = user['PassWord']
    Payment_password = user['Payment_password']
    Game = user['Game']
    Product = user['Product']

    a = Log_in(web=Browser(),user=id,password=password)
    Scan(web=a, Game=Game, Article = Product, Price="1", Passwd=Payment_password)
