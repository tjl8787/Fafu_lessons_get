# Fafu_lessons_get
**只作学习之用**  
当前5.1版本共三个模块：  
>>1.爬虫及通知模块  
>>>>爬取可报名会议  
>>>>群发邮件  
>>2.数据库监视模块  
>>>>临近日期提醒  
>>>>到期删除提醒  
>>3.数据库操作模块  
>>>>实时数据库和备份数据库用户信息的增删改  
大致流程为：  
>>>>通过数据库操作模块录入用户邮箱等信息，爬虫模块爬取到对应的研究生管理系统里的可报名学术会议信息，自动扫描数据库中已保存的用户邮箱，进行群发邮件提醒，
数据库监视模块在此期间对数据库内用户的使用期限进行监控，一旦临近截止日期或到达截止日期，会进行邮件提示  
使用时：  
>>>>同时开启三个python文件，注意个人账号，邮箱，数据库连接，以及其他一些参数的设置  
