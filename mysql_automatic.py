from pymysql import Connection
from datetime import datetime, timedelta, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
import re
from bs4 import BeautifulSoup
import requests
from lxml import etree
from pymysql import Connection



mysql_db_name = "consumer_test"
mysql_db_chart_name = 'test_org'
mysql_db_chart_name2 = "test_lessons"
conn = Connection(
    host='localhost',  # 主机名(ip)
    port=3306,  # 端口
    user='root',  # 账户名
    password='root',  # 密码
    autocommit=True  # 设置自动提交
)
# 写信邮箱的授权码
smtp_self = "crcvdjrwmbjpbefd"
# 管理系统账号密码
tbxUserID_self = "5221139005"
InputPwd_self = "Tjl6972658"
# 发送给单个用户用这个
qq_mail = "1010062249@qq.com"
set_tip_day=3
tbxUserID_self = "5221139012"
InputPwd_self = "Kang.123"

a = True
# 整体工作起始时间
DAY_START = time(7, 00)
DAY_START2= time(21, 00)
# 整体工作结束时间
DAY_END = time(8, 00)
DAY_END2= time(22, 00)


def send_qqEmail(to, code):
    mail_address = "smtp.qq.com"
    mail_port = "25"
    mail_user = "669338120@qq.com"
    mail_pass = smtp_self

    from_address = mail_user
    # to_address = ",".join(to)
    msg = MIMEText('当前检测到: ' + code, 'plain', 'utf-8')

    msg['From'] = "学术会议小助手"
    msg['To'] = ",".join(to)
    subject = "学术会议信息提示"
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_address, mail_port)
        smtp.login(mail_user, mail_pass)
        # smtp.send_message(msg, from_address, to_address)
        smtp.sendmail(from_address, to, str(msg))
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        return False
    return True

# 该函数可以将到期用户进行删除,并提醒
def mysql_judge():
    # 检查连接是否断开，如果断开就进行重连
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name}")
    results: tuple = cursor.fetchall()
    time_now_org = datetime.now()
    # time_now = time_now_org.strftime("%Y-%m-%d %H:%M:%S")
    # print(time_now_org.day)
    for r in results:
        # print(r[2].day)
        # if r[2].year==t2ime_now_org.year and r[2].month==time_now_org.month and r[2].day==time_now_org.day and r[2].hour==time_now_org.hour:
        #     cursor.execute(f"delete from {mysql_db_chart_name} where consumer='{r[0]}'")
        if r[2].year == time_now_org.year and r[2].month == time_now_org.month and r[2].day == time_now_org.day:
            mail=[f'{r[3]}']
            send_qqEmail(mail,
                         f"您的会议小助手使用期限已到期\n起始使用时间:{r[1].year}-{r[1].month}-{r[1].day}\n到期时间:{r[2].year}-{r[2].month}-{r[2].day}\n若需续用请联系管理员，期待您的下次使用！")
            cursor.execute(f"delete from {mysql_db_chart_name} where consumer='{r[0]}'")
            print(f"{r[0]}所在相关数据条已删除")


def mysql_tip():
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    print("成功进入数据库")
    cursor.execute(f"select * from {mysql_db_chart_name} ")
    print("成功搜索数据表")
    results: tuple = cursor.fetchall()
    time_now_org = datetime.now()
    for r in results:
        tip_day = r[2] - timedelta(days=set_tip_day)
        if r[4] == str(
                0) and time_now_org.year == tip_day.year and time_now_org.month == tip_day.month and time_now_org.day >= tip_day.day and time_now_org.day < \
                r[2].day:
            tip_day_now = r[2].day - time_now_org.day
            print(tip_day)
            cursor.execute(f"update {mysql_db_chart_name} set if_tip='1' where consumer='{r[0]}'")
            mail=[f'{r[3]}']
            send_qqEmail(mail,
                         f"\n您的会议小助手使用期限还有不足{tip_day_now}天即将到期\n起始使用时间：{r[1].year}-{r[1].month}-{r[1].day}\n到期时间：{r[2].year}-{r[2].month}-{r[2].day}\n若需延长使用时间请联系管理员！")
# 返回数据库所有人的邮箱
def mysql_monitor():
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name}")
    email_list = []
    results: tuple = cursor.fetchall()
    for r in results:
        # 将多个字符串类型的邮箱地址依次存储进列表，列表中各元素仍为字符串的写法如下，若只是单个则可参考mysql_insert的写法
        email_list.append(list(r)[3])
        # print(r[4]+"类型"+str(type(r[4])))
    print(f"触发群发邮件功能，当前存储邮箱数目为：{len(email_list)}，已作为群发email地址")

    return email_list

def mysql_monitor_lessons_update(name:str, time:str, place:str):
    # print(name)
    # print(time)
    # print(place)
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name2}")
    # print("11111")
    results: tuple = cursor.fetchall()
    for r in results:
        if str(name) == str(r[0]) and str(time) == str(r[1]) and str(place) == str(r[2]):
            print(f"{r[0]},该会议信息正常")

        elif str(name) == str(r[0]) and str(time) == str(r[1]) and str(place) != str(r[2]):

            send_qqEmail(mysql_monitor(),
                         f"个别会议属性出现变动!!!\n名字为：{r[0]}\n会议时间为:{r[1]}\n原会议地点为:{r[2]}\n现会议地点改为:{place}\n新功能试运行，小助手在此提示您稍加留意~")
            print(f"会议地点更改，需发邮件进行通知")
            cursor.execute(
                f"update {mysql_db_chart_name2} set place='{place}' where name='{r[0]}'")


        elif str(name) == str(r[0]) and str(place) == str(r[2]) and str(time) != str(r[1]):
            send_qqEmail(mysql_monitor(),
                         f"个别会议属性出现变动!!!\n名字为：{r[0]}\n会议地点为:{r[2]}\n原会议时间为:{r[1]}\n现会议时间改为:{time}\n新功能试运行，小助手在此提示您稍加留意~")
            print(f"会议时间更改，须发邮件进行通知")
            cursor.execute(
                f"update {mysql_db_chart_name2} set time='{time}' where name='{r[0]}'")

        elif str(time) == str(r[1]) and str(place) == str(r[2]) and str(name) != str(r[0]):
            send_qqEmail(mysql_monitor(),
                         f"个别会议属性出现变动!!!\n原名字为：{r[0]}\n现名字改为:{name}\n会议地点为:{r[2]}\n会议时间为:{r[1]}\n新功能试运行，小助手在此提示您稍加留意~")
            print(f"会议名字更改，需发邮件进行通知")
            cursor.execute(
                f"update {mysql_db_chart_name2} set name='{name}' where name='{r[0]}'")

def crawler():
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
    soup = etree.HTML(rep)
    # print(soup)
    # 此变量存着各个会议的所有信息
    for n in range(1,5):
        context_name = soup.xpath(
            f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[1]/text()")
        # print(f"{str(context_name[0])}")
        # 可报名会议的开会时间，类型为列表，只有一个元素
        context_classtime = soup.xpath(
            f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[2]/text()")
        # print(context_classtime)
        # 可报名会议的开会地点，类型为列表，只有一个元素
        context_location = soup.xpath(
            f"/html/body/form/div[@id='mainframeDiv']/div[@id='divContent']/table[@border='1px']/tr[@onmouseover][{n}]/td[3]/text()")
        # print(context_location)

        mysql_monitor_lessons_update(str(context_name[0]),str(context_classtime[0]),str(context_location[0]))



try:
    while a:
        # 获取当前时间（时，分，秒，微秒）
        current_time = datetime.now().time()
        # 将该时间的时和分作为参数输入time时间戳中
        rel_time = time(current_time.hour, current_time.minute)
        if DAY_START <= rel_time <= DAY_END:
            crawler()
            mysql_tip()
            mysql_judge()
            if conn.open:
                conn.close()
            print(f"开始读取数据库用户，当前时间{rel_time}")
            sleep(3600)
        elif DAY_START2 <= rel_time <= DAY_END2:
            print(f"开始读取数据库用户，当前时间{rel_time}")
            crawler()
            if conn.open:
                conn.close()
            sleep(3600)
except Exception:
    send_qqEmail(qq_mail,f"数据库读取出现问题,当前时间{rel_time},请速去查看")