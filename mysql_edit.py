# -*- coding = utf-8 -*-
# @Project -> File: fafu_lesson_get -> sql_test
# @Time    : 2023/1/24 19:40
# @Author  : 田某人
# @Software: PyCharm
# from pymysqlpool.pool import Pool
from datetime import datetime, timedelta, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from PyMysqlPool.pool import Pool

mysql_db_name = "consumer_test"
# mysql_db_chart_name = 'test_org'
mysql_db_chart_name = 'test'
# mysql_db_chart_name_backups = 'test_backups'
mysql_db_chart_name_backups = 'copy_test'
# 数据库配置
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "db": f"{mysql_db_name}",
    "autocommit": True
}
pool = Pool(**config)
pool.init()

def get_connection():
    return pool.get_conn()

# 邮件配置
smtp_self = "pmkonllcsdzkbaid"
smtp_mail = "669338120@qq.com"

def send_qqEmail(to, code):
    mail_address = "smtp.qq.com"
    mail_port = "25"
    mail_user = smtp_mail
    mail_pass = smtp_self
    from_address = mail_user
    to_address = to
    msg = MIMEText('当前检测到: ' + code, 'plain', 'utf-8')
    msg['From'] = '"=?utf-8?B?5a2m5pyv5Lya6K6u5bCP5Yqp5omL?="<669338120@qq.com>'
    msg['To'] = ",".join(to_address)
    subject = "学术会议信息提示"
    msg['Subject'] = Header(subject, 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_address, mail_port)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(from_address, to, str(msg))
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        return False
    return True

def mysql_insert(insert_name, mail, day_num):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        conn.begin()  # 开始事务
        cursor.execute(f"select * from {mysql_db_chart_name}")
        results = cursor.fetchall()
        # print(results)
        print(type(results))

        for r in results:
            print(r)
            # 此处返回r是一个字典
            if r['consumer'] == insert_name:
                is_input1 = input("数据库中有此人信息是否更新其使用期限(y/n):")
                if is_input1 == 'y':
                    if mail != r['mail']:
                        is_input2 = input("数据库中此人邮箱与本次输入不符，是否更改邮箱(y/n):")
                        if is_input2 == 'y':
                            mysql_update1(conn,insert_name, day_num, mail)
                        if is_input2 == 'n':
                            mysql_update(conn,insert_name, day_num)
                    elif mail == r['mail']:
                        mysql_update(conn,insert_name, day_num)
                    break
                if is_input1 == 'n':
                    print("本次不更新其使用期限")
        print("数据库中无此人信息，已添加新用户")
        if not cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{insert_name}'"):
            time_now_org = datetime.now()
            print(f"当前时间：{time_now_org}")
            begin_time = time_now_org.strftime("%Y-%m-%d %H:%M:%S")
            end_time = time_now_org + timedelta(days=day_num)
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"新用户添加时间：{begin_time}")
            cursor.execute(f"insert into {mysql_db_chart_name}(consumer,begin_time,end_time,mail,if_tip) values('{insert_name}','{begin_time}','{end_time}','{mail}','0')")
            cursor.execute(f"insert into {mysql_db_chart_name_backups}(consumer,begin_time,end_time,mail,if_tip) values('{insert_name}','{begin_time}','{end_time}','{mail}','0')")
            print("新用户添加成功")
            mail = [f'{mail}']
            cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{insert_name}'")
            results: tuple = cursor.fetchall()
            # for r in results:
            #     print(r)
            send_qqEmail(mail,f"您的会议小助手服务已经激活\n服务应用时长：{day_num}天\n起始使用时间：{results['begin_time'].year}-{results['begin_time'].month}-{results['begin_time'].day}\n到期时间：{results['end_time'].year}-{results['end_time'].month}-{results['end_time'].day}\n在此期间小助手会将遇到的所有可报名的野生会议通过邮件方式提醒您关注，若有心仪的会议您可以通过登入学校管理系统自行捕获！")
        conn.commit()  # 提交事务
    except Exception as e:
        conn.rollback()  # 事务回滚
        print("添加用户操作失败：", e)
    finally:
        cursor.close()
        pool.release(conn)  # 释放连接

# mysql_update and mysql_update1 would be similar, including transaction handling and connection management.
# 该函数可以更新用户使用期限
def mysql_update(conn,consumer, day_num):
    conn.ping(reconnect=True)
    cursor = conn.cursor()

    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改前：{r}")
        end_time_org = r['end_time']
        end_time = r['end_time'] + timedelta(days=day_num)
        end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        mail =r['mail']
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
        mail=[f'{r["mail"]}']
        send_qqEmail(mail,
                     f"\n您的会议小助手使用期限已在原有基础上延长{day_num}天\n起始使用时间为：{r['begin_time'].year}-{r['begin_time'].month}-{r['begin_time'].day}\n原到期时间为：{end_time_org.year}-{end_time_org.month}-{end_time_org.day}\n延长后到期时间为：{r['end_time'].year}-{r['end_time'].month}-{r['end_time'].day}\n感谢您对小助手的支持！")
    # conn.close()
# 因为Python没有重载函数这一写法，故新建了一个update函数，意在解决mail有改动情况
def mysql_update1(conn,consumer, day_num,mail):
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    conn.select_db(mysql_db_name)
    cursor.execute(f"select * from {mysql_db_chart_name} where consumer='{consumer}'")
    results: tuple = cursor.fetchall()
    for r in results:
        print(f"修改前：{r}")
        end_time_org = r['end_time']
        end_time = r['end_time'] + timedelta(days=day_num)
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
                     f"\n您的会议小助手使用期限已在原有基础上延长{day_num}天\n起始使用时间为：{r['begin_time'].year}-{r['begin_time'].month}-{r['begin_time'].day}\n原到期时间为：{end_time_org.year}-{end_time_org.month}-{end_time_org.day}\n延长后到期时间为：{r['end_time'].year}-{r['end_time'].month}-{r['end_time'].day}\n感谢您对小助手的支持！")

# 主循环逻辑保持不变
try:
    while True:
        print("欢迎使用数据库操作脚本！")
        print("-------------数据库操作系统---------------")

        print("1.添加或更新数据信息")
        print("2.管理数据库(自动运行)")
        print("3.终止程序运行")
        num = input("请输入序号以使用对应功能：")
        if num == str(1):
            insert_name = input("请输入客户名：")
            mail = input("请输入客户邮箱：")
            day_num = input("请输入客户使用天数：")
            mysql_insert(insert_name, mail, int(day_num))

        elif num == str(3):

            reconfirmation = input("确定退出（Y/N）:")
            if reconfirmation == "Y":
                break
            else:
                continue
except Exception as e:
    print("程序运行出现错误！", e)
finally:
    pool.destroy() # Close the pool when the program is terminated
    print("关闭")
