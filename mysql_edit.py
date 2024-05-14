# -*- coding = utf-8 -*-
# @Project -> File: fafu_lesson_get -> sql_test
# @Time    : 2023/1/24 19:40
# @Author  : 田某人
# @Software: PyCharm
from pymysql import Connection
from datetime import datetime, timedelta, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
import threading

# insert_name="小李"
mysql_db_name = "consumer_test"
mysql_db_chart_name = 'test_org'
mysql_db_chart_name_backups = 'test_backups'
conn = Connection(
    host='localhost',  # 主机名(ip)
    port=3306,  # 端口
    user='root',  # 账户名
    password='root',  # 密码
    autocommit=True  # 设置自动提交
)
set_tip_day = 5
# cursor=conn.cursor()
# conn.select_db("consumer_test")
# time_now_org=datetime.now()
# time_now=time_now_org.strftime("%Y-%m-%d %H:%M:%S")
# time_future=time_now_org+timedelta(days=30)
# time_future=time_future.strftime("%Y-%m-%d %H:%M:%S")
# print(time_future)
# # print(f"{time_naw.hour},{time_naw.minute},{time_naw.second}")
# # print(time_naw)
# # cursor.execute(f"insert into test1(consumer,time) values('{insert_name}','{time_future}')")
# cursor.execute("select * from test1")
# results:tuple=cursor.fetchall()
# for r in results:
#     print(r[1])
#     # if datetime.now().time()<()
# conn.close()
# 发送给单个用户用这个
qq_mail = "1010062249@qq.com"
# 群发用户用这个
email_list = ["1010062249@qq.com"]
# 写信邮箱的授权码
smtp_self = "crcvdjrwmbjpbefd"
# 管理系统账号密码
tbxUserID_self = ""
InputPwd_self = ""


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


# 该函数可以增添新用户
def mysql_insert(insert_name, mail, day_num):

    # 检查连接是否断开，如果断开就进行重连
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    # print(f"{time_naw.hour},{time_naw.minute},{time_naw.second}")
    # print(time_naw)

    cursor.execute(f"select * from {mysql_db_chart_name}")
    results: tuple = cursor.fetchall()
    for r in results:
        # print(type(r[0]) + "1111" + type(insert_name))
        if r[0] == insert_name:
            is_input1=input("数据库中有此人信息是否更新其使用期限(y/n):")
            if is_input1==str('y'):
                # print(type(r[3]))
                # print(type(mail))
                if mail!=r[3]:
                    is_input2=input("数据库中此人邮箱与本次输入不符，是否更改邮箱(y/n):")
                    if is_input2=='y':
                        # print("1")
                        mysql_update1(insert_name, day_num,mail)
                    if is_input2=='n':
                        # print("2")
                        mysql_update(insert_name,day_num)
                elif mail==r[3]:
                    # print("3")
                    mysql_update(insert_name,day_num)


                break
            if is_input1=='n':
                print("本次不更新其使用期限")
    if not cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{insert_name}'"):
        time_now_org = datetime.now()
        begin_time = time_now_org.strftime("%Y-%m-%d %H:%M:%S")
        end_time = time_now_org + timedelta(days=day_num)
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        print(end_time)
        cursor.execute(
            # 改写法可适用于正常插入时，若数据库中已有存此项数据信息，则对需要修改的项进行更新
            # f"insert into {mysql_db_chart_name}(consumer,begin_time,end_time,mail) values('{insert_name}','{begin_time}','{end_time}','{mail}') on duplicate key update end_time='{end_time}',mail='{mail}'")
            f"insert into {mysql_db_chart_name}(consumer,begin_time,end_time,mail,if_tip) values('{insert_name}','{begin_time}','{end_time}','{mail}','0')"
        )
        cursor.execute(
            f"insert into {mysql_db_chart_name_backups}(consumer,begin_time,end_time,mail,if_tip) values('{insert_name}','{begin_time}','{end_time}','{mail}','0')"
        )

        cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{insert_name}'")
        results: tuple = cursor.fetchall()
        for r in results:
            print(list(r[3]))
        # 只将一个字符串类型邮箱地址转换成列表存储字符串形式为该写法，若为列表中存储多个字符串类型的邮箱地址可参考mysql_monitor中对应位置写法
        mail = [f'{mail}']
        send_qqEmail(mail,f"您的会议小助手服务已经激活\n服务应用时长：{day_num}天\n起始使用时间：{results[0][1].year}-{results[0][1].month}-{results[0][1].day}\n到期时间：{results[0][2].year}-{results[0][2].month}-{results[0][2].day}\n在此期间小助手会将遇到的所有可报名的野生会议通过邮件方式提醒您关注，若有心仪的会议您可以通过登入学校管理系统自行捕获！")
        print("邮件发送成功")
        # if datetime.now().time()<()



# 该函数可以将到期用户进行删除,并提醒
def mysql_judge():
    #检查连接是否断开，如果断开就进行重连
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
                         f"您的会议小助手使用期限已到期\n起始使用时间:{r[1].year}-{r[1].month}-{r[1].day}\n到期时间:{r[2].year}-{r[2].month}-{r[2].day}\n若需续费请联系管理员，期待您的下次使用！")
            cursor.execute(f"delete from {mysql_db_chart_name} where consumer='{r[0]}'")
            print(f"{r[0]}所在相关数据条已删除")



# 该函数可以对即将到期的用户进行提醒
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


# 该函数可以更新用户使用期限
def mysql_update(consumer, day_num):
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改前：{r}")
        end_time_org = r[2]
        end_time = r[2] + timedelta(days=day_num)
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        mail =r[3]
        print(mail)
        # update同一个表格多值修改
        cursor.execute(f"update {mysql_db_chart_name} set end_time='{end_time}',if_tip='0' where consumer='{consumer}'")
        # 当mail改动，在备份表中直接添加改动后的新记录
        print("实时表成功更新")
        cursor.execute(
            f"insert into {mysql_db_chart_name_backups}(consumer,begin_time,end_time,mail,if_tip) values('{consumer}','{end_time_org}','{end_time}','{mail}','0')")
        print("备份表已实时添加新操作")
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改后：{r}")
        mail=[f'{r[3]}']
        send_qqEmail(mail,
                     f"\n您的会议小助手使用期限已在原有基础上延长{day_num}天\n起始使用时间为：{r[1].year}-{r[1].month}-{r[1].day}\n原到期时间为：{end_time_org.year}-{end_time_org.month}-{end_time_org.day}\n延长后到期时间为：{r[2].year}-{r[2].month}-{r[2].day}\n感谢您对小助手的支持！")
    # conn.close()
# 因为Python没有重载函数这一写法，故新建了一个update函数，意在解决mail有改动情况
def mysql_update1(consumer, day_num,mail):
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改前：{r}")
        end_time_org = r[2]
        end_time = r[2] + timedelta(days=day_num)
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        # update同一个表格多值修改
        cursor.execute(f"update {mysql_db_chart_name} set end_time='{end_time}',mail='{mail}',if_tip='0' where consumer='{consumer}'")
        print("实时表成功更新")
        # 当mail改动，在备份表中直接添加改动后的新记录
        cursor.execute(f"insert into {mysql_db_chart_name_backups}(consumer,begin_time,end_time,mail,if_tip) values('{consumer}','{end_time_org}','{end_time}','{mail}','0')")
        print("备份表已实时添加新操作")
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改后：{r}")
        mail=[f'{r[3]}']
        send_qqEmail(mail,
                     f"\n您的会议小助手使用期限已在原有基础上延长{day_num}天\n起始使用时间为：{r[1].year}-{r[1].month}-{r[1].day}\n原到期时间为：{end_time_org.year}-{end_time_org.month}-{end_time_org.day}\n延长后到期时间为：{r[2].year}-{r[2].month}-{r[2].day}\n感谢您对小助手的支持！")

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
        print(r[3]+"类型"+str(type(r[4])))
    print(email_list)
    print(f"当前存储邮箱数目为：{len(email_list)}，已作为群发email地址")
    return email_list


# mysql_judge()
# mysql_tip()
# mysql_update('小明',10)
a = True
# 工作起始时间
DAY_START = time(11, 00)
# 工作结束时间
DAY_END = time(12, 00)

# 发送给单个用户用这个
qq_mail = "1010062249@qq.com"



try:
    # t1 = threading.Thread(target=mysql_tip(), args=("thread 1",))
    # t2 = threading.Thread(target=mysql_judge(), args=("thread 2",))
    # t = [t1, t2]

    while a:
        # t1.start()
        # t2.start()
        # t1.join()
        # t2.join()
        # sleep(6)
        print("欢迎使用数据库操作脚本！")
        print("-------------数据库操作系统---------------")

        print("1.添加或更新数据信息")
        print("2.管理数据库(自动运行)")
        print("3.终止程序运行")
        num=input("请输入序号以使用对应功能：")
        if num==str(1):
            insert_name=input("请输入客户名：")
            mail=input("请输入客户邮箱：")
            day_num=input("请输入客户使用天数：")
            mysql_insert(insert_name,mail,int(day_num))
            if conn.open:
                conn.close()
        # elif num==str(2):
        #     # 获取当前时间（时，分，秒，微秒）
        #     current_time = datetime.now().time()
        #     # 将该时间的时和分作为参数输入time时间戳中
        #     rel_time = time(current_time.hour, current_time.minute)
        #     while DAY_START <= rel_time <= DAY_END:
        #     # while rel_time :
        #         print(f"开始读取数据库用户,当前时间{rel_time}")
        #         mysql_tip()
        #         mysql_judge()
        #         sleep(3600)
        elif num==str(3):
            if conn.open:
                conn.close()
            reconfirmation=input("确定退出（Y/N）:")
            if reconfirmation=="Y":

                break
            else:
                continue

except Exception:
    print("程序运行出现错误！")
    send_qqEmail(qq_mail,
                 "数据库操作系统出现问题，程序终止运行，请排查问题原因。")
finally:
    if conn.open:
        conn.close()
    print("程序停止运行")


# 测试专用
# while a:
#         # t1.start()
#         # t2.start()
#         # t1.join()
#         # t2.join()
#         # sleep(6)
#         print("欢迎使用数据库操作脚本！")
#         print("-------------数据库操作系统---------------")
#
#         print("1.添加或更新数据信息")
#         print("2.管理数据库(自动运行)")
#         print("3.终止程序运行")
#         num=input("请输入序号以使用对应功能：")
#         if num==str(1):
#             insert_name=input("请输入客户名：")
#             mail=input("请输入客户邮箱：")
#             day_num=input("请输入客户使用天数：")
#             mysql_insert(insert_name,mail,int(day_num))
#         # elif num==str(2):
#         #     # 获取当前时间（时，分，秒，微秒）
#         #     current_time = datetime.now().time()
#         #     # 将该时间的时和分作为参数输入time时间戳中
#         #     rel_time = time(current_time.hour, current_time.minute)
#         #     while DAY_START <= rel_time <= DAY_END:
#         #     # while rel_time :
#         #         print(f"开始读取数据库用户,当前时间{rel_time}")
#         #         mysql_tip()
#         #         mysql_judge()
#         #         sleep(3600)
#         elif num==str(3):
#             reconfirmation=input("确定退出（Y/N）:")
#             if reconfirmation=="Y":
#                 break
#             else:
#                 continue
