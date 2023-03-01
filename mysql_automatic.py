from pymysql import Connection
from datetime import datetime, timedelta, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep
mysql_db_name = "consumer_test"
mysql_db_chart_name = 'test_org'
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
    conn.close()

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
a = True
# 工作起始时间
DAY_START = time(11, 00)
# 工作结束时间
DAY_END = time(12, 00)

try:
    while a:
        # 获取当前时间（时，分，秒，微秒）
        current_time = datetime.now().time()
        # 将该时间的时和分作为参数输入time时间戳中
        rel_time = time(current_time.hour, current_time.minute)
        if DAY_START <= rel_time <= DAY_END:
            mysql_tip()
            mysql_judge()
            print(f"开始读取数据库用户，当前时间{rel_time}")
            sleep(3600)
except Exception:
    send_qqEmail(qq_mail,f"数据库读取出现问题,当前时间{rel_time},请速去查看")