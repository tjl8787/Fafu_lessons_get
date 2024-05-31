# -*- coding = utf-8 -*-
# coding=UTF8


# @Project -> File: Fafu_lessons -> mian
# @Time    : 2022/11/8 18:20
# @Author  : 田某人
# @Software: PyCharm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager#自动下载chromedriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from datetime import time, datetime
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from lxml import etree
from pymysql import Connection

# 发送单个用户用这个
qq_mail = ["1010062249@qq.com"]
# 发送新用户用这个
qq_mail_new = ["2499129400@qq.com"]
# vip群发位
# mail_list_vip = ["1010062249@qq.com", "809465946@qq.com"]
mail_list_vip = ["1010062249@qq.com"]
# 群发多个用户用这个(康正，师姐，治方师兄，彩钰，张伟，常总,大师兄,学委，智伟师兄)
# mail_list=["755053559@qq.com","wyt9954@163.com","1298781107@qq.com","1724346589@qq.com","840060004@qq.com","1471971635@qq.com","1063293223@qq.com","2323878901@qq.com","2499129400@qq.com","878901@qq.com","chang_xin_yue@163.com","1530321648@qq.com","834091686@qq.com"]


# mail_all_list=["1010062249@qq.com","809465946@qq.com","755053559@qq.com","wyt9954@163.com","1724346589@qq.com","1298781107@qq.com","840060004@qq.com","1471971635@qq.com","1063293223@qq.com","2323878901@qq.com","2499129400@qq.com"]

# 起始发送邮箱
smtp_mail = "669338120@qq.com"
# 起始发送邮箱的授权码
smtp_self = "pmkonllcsdzkbaid"
tbxUserID_self = "1221193002"
InputPwd_self = "Qcyg8008208820"
# tbxUserID_self = "5221139012"
# InputPwd_self = "Kang.123"
user_name="5221139005"
user_password="Tjl6972658"

# 邮件发送函数
def send_qqEmail(to, code):
    mail_address = "smtp.qq.com"
    mail_port = "25"
    mail_user = smtp_mail
    mail_pass = smtp_self

    from_address = mail_user
    to_address = to
    msg = MIMEText('当前检测到: ' + code, 'plain', 'utf-8')
    # msg['From'] = "学术会议小助手"
    msg['From'] = '"=?utf-8?B?5a2m5pyv5Lya6K6u5bCP5Yqp5omL?="<669338120@qq.com>'

    # 群发时要和sendmail函数中的发送地址保持一个是列表一个是字符串的区别
    msg['To'] = ",".join(to_address)

    subject = "学术会议信息提示"
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_address, mail_port)
        smtp.login(mail_user, mail_pass)
        # smtp.send_message(msg, from_address, to_address)
        # 这里一定要注意msg要是字符串类型
        # print("1234545")
        smtp.sendmail(from_address, to, str(msg))
        # print("1234545")
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        return False
    return True


mysql_db_name = "consumer_test"
mysql_db_chart_name="test_org"
mysql_db_chart_name_backups="test_backups"
mysql_db_chart_name_test="test"
mysql_db_chart_name_test_backups="copy_test"
mysql_db_chart_name2 = "test_lessons"
conn = Connection(
    host='localhost',  # 主机名(ip)
    port=3306,  # 端口
    user='root',  # 账户名
    password='root',  # 密码
    autocommit=True  # 设置自动提交
)
# 该函数负责向数据库添加课程名称和加入的时间
# def mysql_insert(insert_name,time):
#     # 检查连接是否断开，如果断开就进行重连
#     conn.ping(reconnect=True)
#     cursor = conn.cursor()
#     conn.select_db(mysql_db_name)
#     # print(f"{time_naw.hour},{time_naw.minute},{time_naw.second}")
#     # print(time_naw)
#     print(f"名字为：{insert_name}，时间为：{time}")
#     cursor.execute(
#         # 改写法可适用于正常插入时，若数据库中已有存此项数据信息，则对需要修改的项进行更新
#         # f"insert into {mysql_db_chart_name}(consumer,begin_time,end_time,mail) values('{insert_name}','{begin_time}','{end_time}','{mail}') on duplicate key update end_time='{end_time}',mail='{mail}'")
#         f"insert into {mysql_db_chart_name2}(name,time) values('{insert_name}','{time}')"
#     )
#     # print("1")
#     print(f"已添加可报名会议进入数据库，名字为：{insert_name}，时间为：{time}")

# 该函数负责向数据库添加课程名称和加入的时间,地点
def mysql_insert_update(insert_name,time,place):
    # 检查连接是否断开，如果断开就进行重连
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    time_now_org = datetime.now()
    current_time_now=time_now_org.strftime("%Y-%m-%d %H:%M:%S")
    # print(f"{time_naw.hour},{time_naw.minute},{time_naw.second}")
    # print(time_naw)
    # print(f"名字为：{insert_name}，时间为：{time}，会议地点为：{place}")
    cursor.execute(
        # 改写法可适用于正常插入时，若数据库中已有存此项数据信息，则对需要修改的项进行更新
        # f"insert into {mysql_db_chart_name}(consumer,begin_time,end_time,mail) values('{insert_name}','{begin_time}','{end_time}','{mail}') on duplicate key update end_time='{end_time}',mail='{mail}'")
        f"insert into {mysql_db_chart_name2}(name,time,place,registration_time) values('{insert_name}','{time}','{place}','{current_time_now}')"
    )
    print("1")
    print(f"已添加可报名会议进入数据库，名字为：{insert_name}，时间为：{time}，会议地点为：{place},记录时间为{current_time}")
# 该函数最终以列表形式返回数据库中存储的邮件
def mysql_monitor():
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name}")
    email_list = []
    results: tuple = cursor.fetchall()
    for r in results:
        get_num = r[5] + 1
        cursor.execute(
            f"update {mysql_db_chart_name} set get_num='{get_num}' where consumer='{r[0]}'")

        cursor.execute(
            f"update {mysql_db_chart_name_backups} set get_num='{get_num}' where consumer='{r[0]}'")
        # 将多个字符串类型的邮箱地址依次存储进列表，列表中各元素仍为字符串的写法如下，若只是单个则可参考mysql_insert的写法
        email_list.append(list(r)[3])
        # print(r[4]+"类型"+str(type(r[4])))
    print(f"当前存储邮箱数目为：{len(email_list)}，已作为群发email地址")
    conn.close()
    return email_list

# 测试用可将上面的注释掉松开这个
# def mysql_monitor():
#     conn.ping(reconnect=True)
#     cursor = conn.cursor()
#     conn.select_db(mysql_db_name)
#     cursor.execute(f"select * from {mysql_db_chart_name_test}")
#     email_list = []
#     results: tuple = cursor.fetchall()
#     for r in results:
#         get_num=r[5]+1
#         cursor.execute(
#             f"update {mysql_db_chart_name_test} set get_num='{get_num}' where consumer='{r[0]}'")
#
#         cursor.execute(
#             f"update {mysql_db_chart_name_test_backups} set get_num='{get_num}' where consumer='{r[0]}'")
#         # 将多个字符串类型的邮箱地址依次存储进列表，列表中各元素仍为字符串的写法如下，若只是单个则可参考mysql_insert的写法
#         email_list.append(list(r)[3])
#         # print(r[4]+"类型"+str(type(r[4])))
#     print(f"当前存储邮箱数目为：{len(email_list)}，已作为群发email地址")
#     conn.close()
#     return email_list



# 该函数负责返回1或0,1为有重复
def mysql_monitor_lessons(name,time):

    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name2}")

    results: tuple = cursor.fetchall()
    for r in results:
        if str(name)==str(r[0]) and str(time)==str(r[1]) :
            print(f"此课程已添加过，无需群发邮件通知")
            return 1
        elif str(name)==str(r[0]) and ((str(r[3])).split('-'))[0]==str(datetime.now().year) and ((str(r[3])).split('-'))[1]==str(datetime.now().month):
            print(f"此课程已添加过，无需群发邮件通知")
            return 1
    print(f"此课程未添加过，需要进行群发邮件通知")
    return 0

# headers={
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "cookie":"ASP.NET_SessionId=23amui45chyrpybnmzjwa145; sdmenu_my_menu=00000000000001000",
#     "Referer":"http://yjsjyglxt.fafu.edu.cn/tbbmgl/bmx_xsbm.aspx?lasturl=/tbbmgl/xs_bmxx_xs.aspx",
#     "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
#     "connection":"keep-alive",
# }
# url ="http://yjsjyglxt.fafu.edu.cn/tbbmgl/bmx_xsbm.aspx?page=1&pageSize=10"
# rep = requests.get(url, headers=headers).content.decode('utf-8')
# print(rep)
# 工作起始时间
DAY_START = time(7, 00)
# 工作结束时间
DAY_END = time(23, 30)

# 加班工作起始时间
DAY_START1 = time(0, 00)
# 加班工作结束时间
DAY_END1 = time(0, 15)

# 程序暂停时间/秒
sleep_time = 900
# 安全启动次数
safe_line = 4
# session安全建立次数
safe_session_line = 2

# 判断是否进入发送下班的判断语句
b = False
# 爬虫之间时间间隔系数，单位每10分钟
num = 1


# 调试的时候一定要把下面这句话注释掉！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# send_qqEmail(qq_mail_new,"\n感谢您的使用，若检测到有野生会议将立刻通知您")
# send_qqEmail(mail_all_list,"\n本学期已结束，感谢您对本脚本的支持。\n11月中旬上线至今，教务系统先后公布了15次学术会议，由于个别时间会议公布过于密集或脚本维护等因素影响，脚本实际已为您捕获并通知了10次学术会议。\n待新学期伊始,学术会议小助手将继续为您服务，期待再次相见！")

j = 0
try:

    while j < safe_line:
        try:
            k = 0
            while k < safe_session_line:
                # 当前时间的时和分，类型为datetime
                current_time = datetime.now().time()
                rel_time = time(current_time.hour, current_time.minute)
                if DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1:

                    print(rel_time)
                    print("上班啦")
                    try:
                        user_agent = UserAgent().chrome
                        print(user_agent)
                        options = webdriver.ChromeOptions()
                        options.add_argument(f"user-agent={user_agent}")
                        bro = webdriver.Chrome(ChromeDriverManager().install())  # 自动匹配chromedriver
                        bro.get(
                            'https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do')
                        bro.maximize_window()
                        sleep(3)
                        try:
                            # 选择登入方式
                            log_select = bro.find_element(By.XPATH,
                                                          '/html/body/div[2]/div/div/div[1]/div/div[3]/form/div/div[2]/div/button/span')
                            log_select.click()
                            sleep(6)
                        except Exception as e:
                            print("本次页面无选择登入方式列表")


                        num_log=1
                        while num_log<=4:
                            try:
                                # 输入账号密码
                                bro.find_element(By.XPATH,
                                                 f'/html/body/div[2]/div/div/div[{num_log}]/div/div[3]/form/div/div[1]/div/div/div/input').send_keys(
                                    f'{user_name}')
                                                # '/html/body/div[2]/div/div/div[1]/div/div[3]/form/div/div[1]/div/div/div/input'
                                                # '/html/body/div[2]/div/div/div[1]/div/div[3]/form/div/div[1]/div/div/div/input'
                                sleep(3)
                                bro.find_element(By.XPATH,
                                                 f'/html/body/div[2]/div/div/div[{num_log}]/div/div[3]/form/div/div[2]/div/div/div/input').send_keys(
                                    f'{user_password}')
                                sleep(3)
                                # 点击确认按钮
                                log = bro.find_element(By.XPATH,
                                                       f"/html/body/div[2]/div/div/div[{num_log}]/div/div[3]/form/div/div[4]/div/button/span")
                                log.click()
                                sleep(6)
                                break
                            except Exception as e:
                                print(f"登入账号密码标签序号改变为{num_log}")
                                num_log += 1
                        # 遇到通知小窗情况
                        try :
                            little_window=bro.find_element(By.XPATH,'/html/body/div[3]/div/div/div[3]/button[1]')
                            if little_window:
                                little_window.click()
                                sleep(6)
                        except Exception as e:
                            print(e)
                        # 活动管理
                        training_management = bro.find_element(By.XPATH,
                                                               '/html/body/div/div/div/div[1]/div[2]/div[4]/div[1]/div[1]/span')

                        # '/html/body/div[1]/div/div/div[1]/div[2]/div[5]/div[1]/div[1]/span')
                        # '/html/body/div/div/div/div[1]/div[2]/div[4]/div[2]/div[12]/div[1]/div[1]/span[1]'
                        training_management.click()
                        sleep(3)
                        # 学术交流
                        # academic_exchange = bro.find_element(By.XPATH,
                        #                                      '/html/body/div/div/div/div[1]/div[2]/div[4]/div[2]/div[13]/div[1]/div[1]/span[2]')
                        academic_exchange = bro.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div[2]/div[4]/div[2]/div[10]/div[1]/div[1]/span[1]')
                                                                   # ‘/html/body/div/div/div/div[1]/div[2]/div[4]/div[2]/div[10]/div[1]/div[1]/span[1]’
                        # '/html/body/div[1]/div/div/div[1]/div[2]/div[5]/div[2]/div[13]/div[1]/div[1]/span[2]')
                        bro.execute_script("arguments[0].scrollIntoView();", academic_exchange)  # 滚动到指定元素
                        academic_exchange.click()
                        sleep(3)
                        # 活动预约
                        event_appointment = bro.find_element(By.XPATH,
                                                             '/html/body/div/div/div/div[1]/div[2]/div[4]/div[2]/div[10]/div[2]/div')

                        event_appointment.click()
                        bro.switch_to.frame(0)  # 切换到iframe
                        # 等待页面加载完全，这里选取了一个标签，一旦它加载成功，说明整个页面加载成功了
                        # WebDriverWait(bro,300).until(EC.presence_of_element_located((By.XPATH,"/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/thead/tr/th[1]")))
                        sleep(6)
                        soup = etree.HTML(bro.page_source)
                        sleep(3)
                    except Exception as e:
                        print(f"未能正常打开chrome，错误为：{e}")
                        bro.quit()
                        # send_qqEmail(qq_mail,
                        #              "未能正常打开chrome\n程序运行时间：%0.2f小时\n当前时间为：%s" % (
                        #                  num * 10 / 60, str(rel_time)))
                        k += 1
                        sleep(600)
                        continue

                    # print(etree.tostring(soup, pretty_print=True, encoding="unicode"))
                    # bro.close()

                    is_susesssful=soup.xpath('/html/body/main/article/h2/text()')
                    if is_susesssful and is_susesssful[0]=="活动预约":
                        # print("成功进入目标位置")
                        # 成功爬取页面时减少一次安全重启次数
                        if j >= 1:
                            j -= 1
                        # 成功爬取页面时减少一次session安全建立次数
                        if k >= 1:
                            k -= 1
                        if b == False:
                            b = True
                    else:
                        print("未能正常进入到活动预约界面")
                                       # 未开放"/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr/td[1]/div/div/a"
                    is_data=soup.xpath('/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr/td/text()')
                    is_data2=soup.xpath('/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/a/text()')
                    # is_data2=soup.xpath('/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[1]/td[1]/div/div/a/text()')


                    if (is_data and is_data[0]!="没有数据显示！" )or(is_data2) :
                        # print(1111111111111111111111111111111)
                        # table_rows = soup.xpath('/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr')

                        table_rows = soup.xpath('/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr')
                        # print(table_rows)
                        i1 = 1
                        for i, _ in enumerate(table_rows, start=1):
                            # sleep(3)
                            a = soup.xpath(
                                # f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/div[2]/table/tbody/tr[{i}]/td[1]/div/div/a[1]/text()')
                                f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[1]/div/div/a/text()')


                            # print(a[0])
                            if a[0] != "预约":
                                context_name = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[4]/span/text()')

                                print(f"n为{i},会议名称为：{context_name[0]}")

                                # 测试时可以把报名改成详细信息，记得下面的n-=1的if语句要注释掉
                            if  a[0] == "预约":
                                # 正常情况i值为详细信息，并与n一一对应，但当有可报名会议时，报名也占一个位数，因此要减一,测试时可以注释掉

                                print("发现可报名会议")
                                # 可报名会议的开会名称，类型为列表，只有一个元素
                                context_name = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[4]/span/text()')
                                print(f"n为{i},会议名为：{context_name[0]}")
                                # 可报名会议地点
                                # context_location = soup.xpath(
                                #     f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[5]/span/text()')
                                # print(f"n为{i},会议地点为：{context_location[0]}")
                                # 可报名会议时间
                                context_classtime = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[6]/span/text()')
                                # print(f"n为{i},会议时间为：{context_classtime[0]}")
                                # 可报名会议学分
                                context_grade = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[12]/span/text()')
                                # print(f"n为{i},会议学分为：{context_grade[0]}")
                                # 可报名会议的其他说明
                                # WebDriverWait(bro, 300).until(EC.presence_of_element_located((By.XPATH,
                                #                                                               "f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[13]/span/@title")))
                                context_ortherins_title=soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[13]/span/@title')
                                context_ortherins_test = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[13]/span/text()')
                                # 其他说明有可能在标签内容里省略，但title属性会有，如果二者都没有则返回自定义字符串
                                if context_ortherins_title != [] and context_ortherins_test != [] and len(
                                        context_ortherins_test[0]) > 0:
                                    context_ortherins = max(context_ortherins_title[0], context_ortherins_test[0],
                                                            key=len)
                                elif context_ortherins_test != [] and len(context_ortherins_test[0]) > 0:
                                    context_ortherins = context_ortherins_test[0]
                                elif context_ortherins_title != [] and len(context_ortherins_title[0]) > 0:
                                    context_ortherins = context_ortherins_title[0]
                                else:
                                    context_ortherins = "暂无说明"
                                # print(f"n为{i},会议其他说明为：{context_ortherins[0]}")
                                # 可报名会议人数
                                context_people = soup.xpath(
                                    f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[2]/div/label/text()')
                                #    "/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr/td[2]/div/label"
                                context_location_pre = bro.find_element(By.XPATH,
                                                                        f'/html/body/main/article/section/div[2]/div[2]/div[1]/div/table/tbody/tr[{i}]/td[1]/div/a')


                                context_location_pre.click()
                                sleep(6)
                                # i1=1
                                while i1<10:
                                    try:
                                        # 可报名会议地点
                                        context_location = bro.find_element(By.XPATH,f'/html/body/div[{6+2*i1}]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p').text

                                                                            # 规律8+(i-1)*2化简6+2*i,经测试为动态生成，只在这个公式的结果集合里随机生成数
                                                                            # "/html/body/div[12]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p"
                                                                            # f'/html/body/div[8]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p').text
                                                                            # "/html/body/div[10]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p"
                                                                            # "/html/body/div[12]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p"
                                                                            #  /html/body/div[8]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p
                                        #                                     /html/body/div[10]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p
                                        #                                     /html/body/div[10]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[9]/div/p
                                        # print(f"{context_location}")
                                        # 可报名学院
                                        context_enrollable_college=bro.find_element(By.XPATH,f'/html/body/div[{6+2*i1}]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[16]/div/p').text
                                        #                                                      /html/body/div[10]/div/div[1]/section/div[2]/div/div[2]/div[2]/div[16]/div/p
                                        college_context_len1=len("农学院, 乡村振兴学院, 园艺学院, 林学院, 生命科学学院, 动物科学学院（蜂学学院）, 动物科学学院（蜂学学院）, 资源与环境学院, 食品科学学院, 材料工程学院, 计算机与信息学院, 机电工程学院, 交通与土木工程学院, 经济与管理学院, 经济与管理学院, 公共管理与法学院, 文法学院, 马克思主义学院, 风景园林与艺术学院, 国际学院(戴尔豪西大学学院), 工商管理硕士（MBA）教育中心, 公共管理硕士（MPA）教育中心, 安溪茶学院（数字经济学院）, 继续教育学院 远程教育学院(合署)　, 海洋学院, 研究生院, 菌草与生态学院, 国际合作与交流处 台港澳事务办公室(合署), 学生工作部, 图书馆, 港澳台高校, 国外高校, 未来技术学院, 中国科学院福建物质结构研究所, 中国科学院城市环境研究所, 植物保护学院")
                                        college_context_len2=len("农学院, 乡村振兴学院, 园艺学院, 林学院, 生命科学学院, 动物科学学院（蜂学学院）, 动物科学学院（蜂学学院）, 资源与环境学院, 食品科学学院, 材料工程学院, 计算机与信息学院, 机电工程学院, 交通与土木工程学院, 经济与管理学院, 经济与管理学院, 公共管理与法学院, 文法学院, 马克思主义学院, 风景园林与艺术学院, 戴尔豪西大学联合学院(国际学院), 工商管理硕士（MBA）教育中心, 公共管理硕士（MPA）教育中心, 安溪茶学院（数字经济学院）, 继续教育学院 远程教育学院(合署), 海洋学院, 研究生院, 菌草与生态学院, 国际合作与交流处 台港澳事务办公室(合署), 学生工作部, 图书馆, 港澳台高校, 国外高校, 未来技术学院, 中国科学院福建物质结构研究所, 中国科学院城市环境研究所, 植物保护学院")
                                        college_context_len3=len("农学院, 乡村振兴学院, 园艺学院, 林学院, 生命科学学院, 动物科学学院, 蜂学与生物医药学院, 资源与环境学院, 食品科学学院, 材料工程学院, 计算机与信息学院, 机电工程学院, 交通与土木工程学院, 经济与管理学院, 经济与管理学院, 公共管理与法学院, 文法学院, 马克思主义学院, 风景园林与艺术学院, 戴尔豪西大学联合学院(国际学院), 工商管理硕士（MBA）教育中心, 公共管理硕士（MPA）教育中心, 安溪茶学院（数字经济学院）, 继续教育学院 远程教育学院(合署), 海洋学院, 研究生院, 菌草与生态学院, 国际合作与交流处 台港澳事务办公室(合署), 学生工作部, 图书馆, 港澳台高校, 国外高校, 未来技术学院, 中国科学院福建物质结构研究所, 中国科学院城市环境研究所, 植物保护学院")
                                        college_context_len4=len("科研处, 人事处 人才办(合署), 离退休干部工作处, 计划财务处, 国有资产管理处, 后勤管理处, 监察处 审计处(合署), 对外联络处 校友会 基金会, 知识产权管理处, 产业处 生产处(合署), 现代教育技术与信息管理中心, 纪委, 党委办公室 校办公室(合署), 组织部, 党校, 宣传部, 统战部, 机关党委, 人武部 保卫处(合署), 教育工会, 团委, 基因组与生物技术研究中心, 海峡创业育成中心, 学报编辑部, 校医院, 计生办, 体育教学部, 国家菌草工程技术研究中心, 金山学院, 国家甘蔗工程技术研究中心, 闽台作物有害生物生态防控国家重点实验室, 社会科学处, 教务处, 农学院, 植物保护学院, 园艺学院, 林学院, 生命科学学院, 动物科学学院, 蜂学与生物医药学院, 资源与环境学院, 食品科学学院, 材料工程学院, 计算机与信息学院, 机电工程学院, 交通与土木工程学院, 经济与管理学院, 经济与管理学院, 公共管理与法学院, 文法学院, 马克思主义学院, 风景园林与艺术学院, 戴尔豪西大学联合学院(国际学院), 工商管理硕士（MBA）教育中心, 公共管理硕士（MPA）教育中心, 安溪茶学院（数字经济学院）, 继续教育学院 远程教育学院(合署), 海洋学院, 研究生院, 菌草与生态学院, 基建处, 国际合作与交流处 台港澳事务办公室(合署), 学生工作部, 图书馆, 港澳台高校, 国外高校, 未来技术学院, 中国科学院福建物质结构研究所, 中国科学院城市环境研究所, 乡村振兴学院")
                                        college_context_len5=len("农学院, 系统预设_测试数据, 园艺学院, 林学院, 生命科学学院, 动物科学学院, 蜂学与生物医药学院, 资源与环境学院, 食品科学学院, 材料工程学院, 计算机与信息学院, 机电工程学院, 交通与土木工程学院, 经济与管理学院, 经济与管理学院, 公共管理与法学院, 文法学院, 马克思主义学院, 风景园林与艺术学院, 戴尔豪西大学联合学院(国际学院), 工商管理硕士（MBA）教育中心, 公共管理硕士（MPA）教育中心, 安溪茶学院（数字经济学院）, 继续教育学院 远程教育学院(合署), 海洋学院, 研究生院, 菌草与生态学院, 国际合作与交流处 台港澳事务办公室(合署), 学生工作部, 图书馆, 港澳台高校, 国外高校, 未来技术学院, 中国科学院福建物质结构研究所, 中国科学院城市环境研究所, 乡村振兴学院, 植物保护学院")
                                        # if len(context_enrollable_college)==college_context_len1 or len(context_enrollable_college)==college_context_len2 or len(context_enrollable_college)==college_context_len3 or len(context_enrollable_college)==college_context_len4 or len(context_enrollable_college)==college_context_len5:
                                        if len(context_enrollable_college)>=college_context_len3:
                                            context_enrollable_college="各校区均可报名!"
                                        else:
                                            context_enrollable_college="仅允许部分学院和机构报名，"+context_enrollable_college
                                        # 返回按钮
                                        # "/html/body/div[12]/div/div[2]/footer/div"
                                        back_button = bro.find_element(By.XPATH, f"/html/body/div[{6+2*i1}]/div/div[2]/footer/div")
                                        back_button.click()
                                        sleep(3)
                                        break
                                        # print(f'{context_enrollable_college}')
                                    except Exception as e:
                                        print(e)
                                        i1+=1


                                is_notice=mysql_monitor_lessons(str(context_name[0]),str(context_classtime[0]))
                                # print("1111111111111111111111111111")
                                if is_notice==0:

                                    # mysql_insert(str(context_name[0]),str(context_classtime[0]))
                                    mysql_insert_update(str(context_name[0]),str(context_classtime[0]),str(context_location))

                                    try:
                                        print(f"当前时间为：{rel_time}")
                                        try:
                                            # 紧急情况用第一个发邮件
                                            # send_qqEmail(mysql_monitor(),
                                            #              f"野生会议已出现!!!\n此为新系统下的会议捕获，目前不断完善中,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people[0]}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")

                                            send_qqEmail(mail_list_vip,
                                                         f"野生会议已出现!!!\n此为新系统下的会议捕获，目前不断完善中，若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people[0]}\n其他说明为:{context_ortherins}\n可报名学院为：{context_enrollable_college}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")

                                            send_qqEmail(mysql_monitor(),
                                                         f"野生会议已出现!!!\n此为新系统下的会议捕获，目前不断完善中,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people[0]}\n其他说明为:{context_ortherins}\n可报名学院为：{context_enrollable_college}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")

                                        except Exception as e:
                                            print(e)
                                            send_qqEmail(mail_list_vip,
                                                         f"野生会议已出现!!!\n此为新系统下的会议捕获，目前不断完善中,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people[0]}\n可报名学院为：{context_enrollable_college}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")

                                            send_qqEmail(mysql_monitor(),
                                                         f"野生会议已出现!!!\n此为新系统下的会议捕获，目前不断完善中,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people[0]}\n可报名学院为：{context_enrollable_college}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")
                                            # print(n)
                                    except Exception:
                                        send_qqEmail(qq_mail, f"野生会议已出现,快枪!!! ")
                                        if context_grade[0] > 0.1:
                                            send_qqEmail(mysql_monitor(),
                                                         f"野生会议已出现但其学分属性较高!!!\n名字为：{context_name[0]} ")
                                            # print(n)
                                        else:
                                            send_qqEmail(mysql_monitor(), f"野生会议已出现!!!\n名字为：{context_name[0]} ")
                                            # print(n)
                                    finally:
                                        print("已检测到会议")
                                elif is_notice == 1:
                                    # print(n)
                                    print("无需进行添加")

                                    # 测试代码，可将上面发邮件的全注释掉解开下面的注释
                                # try:
                                #     print(f"当前时间为：{rel_time}")
                                #     try:
                                #
                                #         send_qqEmail(qq_mail,
                                #                      f"野生会议已出现!!!\n此为新系统下的会议捕获，尚不稳定,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people}\n其他说明为:{context_ortherins[0]}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")
                                #
                                #     except Exception:
                                #
                                #         send_qqEmail(qq_mail,
                                #                      f"野生会议已出现!!!\n此为新系统下的会议捕获，尚不稳定,若有问题欢迎同小助手反馈,qq，频道，邮箱均可\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location}\n会议学分为:{context_grade[0]}\n当前报名人数情况为:{context_people}\n请点击链接登入教育管理系统捕获该会议：https://yjsapp.fafu.edu.cn/gsapp/sys/yjsrzfwapp/dbLogin/main.do?redirectUrl=https%3A%2F%2Fyjsapp.fafu.edu.cn%2Fgsapp%2Fsys%2Fyjsemaphome%2Fportal%2Findex.do")
                                #         # print(n)
                                # except Exception:
                                #     send_qqEmail(qq_mail, f"野生会议已出现,快枪!!! ")
                                #     if context_grade[0] > 0.1:
                                #         send_qqEmail(mysql_monitor(),
                                #                      f"野生会议已出现但其学分属性较高!!!\n名字为：{context_name[0]} ")


                    else:
                        print("暂无会议数据显示")
                    bro.quit()
                    # 当前时间的时和分，类型为datetime
                    current_time = datetime.now().time()
                    rel_time = time(current_time.hour, current_time.minute)
                    if DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1:
                        if conn.open:
                            conn.close()
                        print("搜索冷却cd中")

                        # 程序每次爬取的时间间隔
                        if DAY_START <= rel_time <= DAY_END:
                            sleep(600)

                            num += 1
                            print("当前已进行%d次搜索，程序运行时间：%0.2f小时" % (num, num * 10 / 60))
                        elif DAY_START1 <= rel_time <= DAY_END1:
                            sleep(300)

                            num += 0.5
                            print("当前已进行%d次搜索，程序运行时间：%0.2f小时" % (num, num * 10 / 60))


                        # 当前时间的时和分，类型为datetime
                        current_time = datetime.now().time()
                        rel_time = time(current_time.hour, current_time.minute)
                    if k>1 and DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1:
                        print(f"网页进入异常，程序重新进入管理系统,当前重新进入管理系统次数为{k}次,当前时间为：{rel_time}")
                        print("当前已进行%d次搜索，程序运行时间：%0.2f小时" % (num, num * 10 / 60))
                        num+=1
                        # send_qqEmail(qq_mail,"Session已失效，程序重新建立session，当前已进行%d次搜索，程序运行时间：%0.2f小时"% (num, num * 10 / 60))

                elif current_time > DAY_END1 and b == True:

                    # send_qqEmail(qq_mail,
                    #          f"已经下班啦,今日下班时间为{rel_time}" )
                    b = False
                    print(f"已经下班啦,,今日下班时间为{rel_time}")
                    # 当前时间的时和分，类型为datetime
            current_time = datetime.now().time()
            rel_time = time(current_time.hour, current_time.minute)
            print(f"异常处理次数超出范围，{sleep_time / 60}分钟后重新进入管理系统，当前时间为{rel_time}")
            sleep(sleep_time / 60)
        except Exception as e:
            print(e)
            j += 1
            # 当前时间的时和分，类型为datetime
            current_time = datetime.now().time()
            rel_time = time(current_time.hour, current_time.minute)
            # send_qqEmail(qq_mail,
            #              "Session建立失败，程序被迫中断，1小时后尝试自动重启，当前已进行%d次搜索，程序运行时间：%0.2f小时，当前时间为：%s,安全重启次数为：%d次" % (
            #                  num, num * 10 / 60, str(rel_time),safe_line))
            b = True
        finally:
            try:
                bro.close()
            finally:
                bro.quit()

            if DAY_START <= rel_time <= DAY_END:
                print(
                    f"管理系统进入失败，程序被迫中断，{sleep_time / 60}分钟后尝试自动重启，当前已进行{num}次搜索，程序运行时间：{(num * 10) / 60}小时，当前时间为：{rel_time},安全重启次数为：{j}次")
                sleep(sleep_time)
            elif DAY_START1 <= rel_time <= DAY_END1:
                # send_qqEmail(qq_mail,
                #              f"紧急情况\nSession建立失败，程序被迫中断\n{sleep_time / 6/60 }分钟后尝试自动重启\n当前已进行{num}次搜索,程序运行时间：{(num * 10) / 60}小时\n当前时间为：{rel_time}\n安全重启次数为：{j}次\n若无手动操作将于{sleep_time /6/60}分钟后，自动重建session")
                print(
                    f"管理系统进入失败，程序被迫中断，{sleep_time / 6/60}分钟后尝试自动重启，当前已进行{num}次搜索，程序运行时间：{(num * 10) / 60}小时，当前时间为：{rel_time},安全重启次数为：{j}次")
                sleep(sleep_time / 6)
    current_time = datetime.now().time()
    rel_time = time(current_time.hour, current_time.minute)
    send_qqEmail(qq_mail,
                 "安全重启次数达到上限，程序出现不可逆错误请管理员手动修复后重新运行本程序。\n程序运行时间：%0.2f小时\n当前时间为：%s" % (
                 num * 10 / 60, str(rel_time)))
    print("进入管理系统失败，程序结束")
except Exception:
    current_time = datetime.now().time()
    rel_time = time(current_time.hour, current_time.minute)
    send_qqEmail(qq_mail,
                 "未知问题，程序出现不可逆错误请管理员手动修复后重新运行本程序。\n程序运行时间：%0.2f小时\n当前时间为：%s" % (
                     num * 10 / 60, str(rel_time)))
