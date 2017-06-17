员工信息表程序说明


一、基本功能
功能介绍：读取员工信息文件，对文件中的员工信息进行增删改查。


二、运行环境
python版本：python 3.6.1


三、移植性
该程序只能在windows系统上运行


四、目录结构及说明
1.目录结构：
员工信息表程序/
|-- staff_table
|
|-- python_sql.py
|
|-- Readme
|
|-- staffTable_flowChart.png

2.目录说明：
staff_table：是员工信息表
python_sql.py：是对员工信息表操作的程序
Readme：员工信息表程序的介绍及施工说明
staffTable_flowChart.png：员工信息表程序运行的流程图


五、运行方式
运行python_sql.py即可


六、程序使用方法
1.增加功能：新增一条员工信息
  insert into staff_table values Joe Zhao,25,18888888888,IT,2017-01-01
  (age、phone、enroll_date需要符合格式，否则会提示无法添加)

2.删除功能：删除一条员工信息
  delete from staff_table where id=6

3.修改功能：修改某个员工信息
  update staff_table set age='20' where name=Joe Zhao

4.查找功能：查找特定条件的员工信息
  select name,age from staff_table where age > 22
  select * from staff_table where dept = "IT"
  select * from staff_table where enroll_date like "2013"
  （符号两边需要打空格）

5.退出程序：输入q退出程序；

七、程序使用知识点
1.python简单数据结构的使用：字符串、整数、列表、字典、布尔值等；
2.python函数的定义及调用；
3.tag标志位的使用；
4.python基本语法的使用:while循环、for循环、if...elif....else....判断；
5.python文件的操作的使用；
