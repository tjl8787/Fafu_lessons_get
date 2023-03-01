# -*- coding = utf-8 -*-
# @Project -> File: Fafu_lessons -> mian
# @Time    : 2022/11/8 18:20
# @Author  : 田某人
# @Software: PyCharm
import re
from datetime import time, datetime
from time import sleep
from bs4 import BeautifulSoup
import requests
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
mail_list_vip = ["1010062249@qq.com", "809465946@qq.com"]
# 群发多个用户用这个(康正，师姐，治方师兄，彩钰，张伟，常总,大师兄,学委，智伟师兄)
# mail_list=["755053559@qq.com","wyt9954@163.com","1298781107@qq.com","1724346589@qq.com","840060004@qq.com","1471971635@qq.com","1063293223@qq.com","2323878901@qq.com","2499129400@qq.com"]


# mail_all_list=["1010062249@qq.com","809465946@qq.com","755053559@qq.com","wyt9954@163.com","1724346589@qq.com","1298781107@qq.com","840060004@qq.com","1471971635@qq.com","1063293223@qq.com","2323878901@qq.com","2499129400@qq.com"]

# 起始发送邮箱
smtp_mail = "669338120@qq.com"
# 起始发送邮箱的授权码
smtp_self = "mtwvnayhbwjnbegi"
tbxUserID_self = "1221193002"
InputPwd_self = "Qcyg8008208820"


# 邮件发送函数
def send_qqEmail(to, code):
    mail_address = "smtp.qq.com"
    mail_port = "25"
    mail_user = smtp_mail
    mail_pass = smtp_self

    from_address = mail_user
    to_address = to
    msg = MIMEText('当前检测到: ' + code, 'plain', 'utf-8')
    msg['From'] = "学术会议小助手"

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
        smtp.sendmail(from_address, to, str(msg))
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        return False
    return True


mysql_db_name = "consumer_test"
mysql_db_chart_name = 'test_org'
conn = Connection(
    host='localhost',  # 主机名(ip)
    port=3306,  # 端口
    user='root',  # 账户名
    password='root',  # 密码
    autocommit=True  # 设置自动提交
)


# 该函数最终以列表形式返回数据库中存储的邮件
def mysql_monitor():
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name}")
    email_list = []
    results: tuple = cursor.fetchall()
    for r in results:
        # 将多个字符串类型的邮箱地址依次存储进列表，列表中各元素仍为字符串的写法如下，若只是单个则可参考mysql_insert的写法
        email_list.append(list(r)[3])
        # print(r[4]+"类型"+str(type(r[4])))
    print(f"当前存储邮箱数目为：{len(email_list)}，已作为群发email地址")
    return email_list


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
DAY_END = time(23, 59)

# 加班工作起始时间
DAY_START1 = time(0, 00)
# 加班工作结束时间
DAY_END1 = time(1, 00)

# 程序暂停时间/秒
sleep_time = 1800
# 安全启动次数
safe_line = 4
# session安全建立次数
safe_session_line = 2

a = True
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
                    print("上班啦")
                    # 创建session对象
                    session = requests.Session()
                    # 管理系统login页面地址
                    url1 = 'http://yjsjyglxt.fafu.edu.cn/login.aspx'
                    # 伪装游客首次读取login页面
                    html_data = session.post(url1)
                    soup = BeautifulSoup(html_data.content, 'html.parser')
                    # 获取必要的动态信息传入到request_data字典中
                    view_state = soup.find(id="__VIEWSTATE")["value"]
                    view_state_encrypted = soup.find(id="__VIEWSTATEENCRYPTED")["value"]
                    # 若未能获取到动态信息说明本次session创建失败，中断程序
                    if not soup.find(id="__VIEWSTATE")["value"]:
                        # 当前时间的时和分，类型为datetime
                        current_time = datetime.now().time()
                        rel_time = time(current_time.hour, current_time.minute, current_time.second)
                        print(
                            "Session建立失败，未获取到对应的属性值，程序被迫中断，后续进入安全启动步骤，当前已进行%d次搜索，程序运行时间：%0.2f小时，当前时间为：%s" % (
                            num, num * 10 / 60, str(rel_time)))
                        # send_qqEmail(qq_mail,
                        #              "Session建立失败，程序被迫中断，当前已进行%d次搜索，程序运行时间：%0.2f小时，当前时间为：%s" % (
                        #              num, num * 10 / 60,str(rel_time)))
                        break
                    # post 要用到的data信息
                    request_data = {
                        "__VIEWSTATE": view_state,
                        "__VIEWSTATEENCRYPTED": view_state_encrypted,
                        "tbxUserID": tbxUserID_self,
                        # "btnLogin.x": "47",#也是动态的，可写死
                        # "btnLogin.y": "28",
                        "btnLogin.x": "0",  # 也是动态的，可写死
                        "btnLogin.y": "0",
                        "InputPwd": InputPwd_self,

                    }
                    # 模拟登入login页面
                    response_data = session.post(url1, data=request_data)
                    # 会议报名页面地址
                    url3 = "http://yjsjyglxt.fafu.edu.cn/tbbmgl/bmx_xsbm.aspx?lasturl=/tbbmgl/xs_bmxx_xs.aspx"
                    # 模拟进入会议报名页面获取页面源代码
                    rep = session.get(url3).content.decode('utf-8')
                    print(rep)
                    k += 1
                    # 监测该页面是否出现可报名的会议
                    while re.search("若报名不参加，请于报名截止日期前一天退出报名，否则将倒扣学术活动分",
                                    rep) is not None and (
                            DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1):
                        # 成功爬取页面时减少一次安全重启次数和session安全建立次数
                        if j >= 1:
                            j -= 1
                        # 成功爬取页面时减少一次session安全建立次数
                        if k >= 1:
                            k -= 1
                        if b == False:
                            b = True
                        soup = etree.HTML(rep)
                        # print(soup)
                        # 此变量存着各个会议的所有信息
                        page = soup.xpath(
                            "/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover]/td/a/text()")
                        # context_name = soup.xpath(
                        #     "/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][2]/td[1]/text()")
                        # context_classtime = soup.xpath(
                        #     "/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][2]/td[2]/text()")
                        # print(context_name)
                        # send_qqEmail("1010062249@qq.com",
                        #              f"野生会议已出现!!!\n名字为：{context_name[0]} \n会议开始时间为:{context_classtime[0]} \n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")
                        # break
                        print(page)
                        n = 1
                        for i in page:
                            if re.search("报名", i) is not None:
                                # print("1111111111111")
                                # 可报名会议的开会名称，类型为列表，只有一个元素
                                context_name = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[1]/text()")
                                # print(context_name)
                                # 可报名会议的开会时间，类型为列表，只有一个元素
                                context_classtime = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[2]/text()")
                                # print(context_classtime)
                                # 可报名会议的开会地点，类型为列表，只有一个元素
                                context_location = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[3]/text()")
                                # print(context_location)
                                # 可报名会议的开会学分，类型为列表，只有一个元素
                                context_grade = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[7]/text()")
                                # print(context_grade)
                                # 剩余可报名人数
                                context_people_total = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[8]/text()")
                                context_people_now = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[9]/text()")
                                context_people=context_people_total-context_people_now
                                # 可报名会议的开会其他说明（比如限定学院优先），类型为列表，只有一个元素
                                context_ortherins = soup.xpath(
                                    f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[10]/text()")
                                try:
                                    try:
                                        send_qqEmail(mail_list_vip,
                                                     f"野生会议已出现!!!\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location[0]}\n会议学分为:{context_grade[0]}\n剩余报名人数为：{context_people}\n其他说明为:{context_ortherins[0]}\n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")

                                        send_qqEmail(mysql_monitor(),
                                                     f"野生会议已出现!!!\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location[0]}\n会议学分为:{context_grade[0]}\n剩余报名人数为：{context_people}\n其他说明为:{context_ortherins[0]}\n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")

                                    except Exception:
                                        send_qqEmail(mail_list_vip,
                                                     f"野生会议已出现!!!\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location[0]}\n会议学分为:{context_grade[0]}\n剩余报名人数为：{context_people}\n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")

                                        send_qqEmail(mysql_monitor(),
                                                     f"野生会议已出现!!!\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location[0]}\n会议学分为:{context_grade[0]}\n剩余报名人数为：{context_people}\n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")
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
                                    print(f"野生会议已出现!!!\n名字为：{context_name[0]}\n剩余报名人数为：{context_people}")
                                    # print(n)
                                    sleep(900)
                                break
                                # 测试代码，可将上面发邮件的全注释掉解开下面的注释
                                # try:
                                #     print(f"野生会议已出现!!!\n名字为：{context_name[0]}\n会议时间为:{context_classtime[0]}\n会议地点为:{context_location[0]}\n会议学分为:{context_grade[0]}\n剩余报名人数为：{context_people}\n请点击链接登入教育管理系统捕获该会议：http://yjsjyglxt.fafu.edu.cn/login.aspx")
                                # finally:
                                #     print("查到会议")
                            n += 1
                        # 当前时间的时和分，类型为datetime
                        current_time = datetime.now().time()
                        rel_time = time(current_time.hour, current_time.minute)
                        if DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1:
                            print("正在搜索中")
                            # 程序每次爬取的时间间隔
                            sleep(600)
                            rep = session.get(url3).content.decode('utf-8')
                            print("当前已进行%d次搜索，程序运行时间：%0.2f小时" % (num, num * 10 / 60))
                            num += 1
                            # 当前时间的时和分，类型为datetime
                            current_time = datetime.now().time()
                            rel_time = time(current_time.hour, current_time.minute)
                    if DAY_START <= rel_time <= DAY_END or DAY_START1 <= rel_time <= DAY_END1:
                        print(f"Session已失效，程序重新建立session,当前session安全建立次数为{k}次")
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
            print(f"session重新建立次数超过安全范围，{sleep_time / 60}分钟后重新建立session，当前时间为{rel_time}")
        except Exception as e:
            j += 1
            # 当前时间的时和分，类型为datetime
            current_time = datetime.now().time()
            rel_time = time(current_time.hour, current_time.minute)
            # send_qqEmail(qq_mail,
            #              "Session建立失败，程序被迫中断，1小时后尝试自动重启，当前已进行%d次搜索，程序运行时间：%0.2f小时，当前时间为：%s,安全重启次数为：%d次" % (
            #                  num, num * 10 / 60, str(rel_time),safe_line))
            print(
                "Session建立失败，程序被迫中断，%d分钟后尝试自动重启，当前已进行%d次搜索，程序运行时间：%0.2f小时，当前时间为：%s,安全重启次数为：%d次" % (
                sleep_time / 60 * 2, num, str(current_time), str(j), safe_line))
            sleep(sleep_time)
            b = True
        finally:
            sleep(sleep_time)
    current_time = datetime.now().time()
    rel_time = time(current_time.hour, current_time.minute)
    send_qqEmail(qq_mail,
                 "安全重启次数达到上限，程序出现不可逆错误请管理员手动修复后重新运行本程序。\n程序运行时间：%0.2f小时\n当前时间为：%s" % (
                 num * 10 / 60, str(rel_time)))
    print("session建立失败，程序结束")
except Exception:
    current_time = datetime.now().time()
    rel_time = time(current_time.hour, current_time.minute)
    send_qqEmail(qq_mail,
                 "未知问题，程序出现不可逆错误请管理员手动修复后重新运行本程序。\n程序运行时间：%0.2f小时\n当前时间为：%s" % (
                     num * 10 / 60, str(rel_time)))