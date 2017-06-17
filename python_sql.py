# Author：zhaoyanqi
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time

def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False

def insert():
    token = 0
    for line in input_list:
        token += 1
    if token == 5:
        insert_info_list = input_list[-1].split(",")
    elif token >5:
        insert_info_list = input_list[-1].split(",")
        insert_info_list[0] = " ".join(input_list[4:-1]) + " " + insert_info_list[0]
    else:
        print("格式错误")
        return
    if input_list[1] == "into" and input_list[3] == "values":
        if input_list[2] == "staff_table":
            input_name = insert_info_list[0]
            while True:#判断年龄格式
                input_age = insert_info_list[1]
                if input_age.isdigit() and len(input_age) == 2:
                    break
                else:
                    print("年龄格式错误")
                    return

            while True:#判断电话格式及
                token = False
                input_phone = insert_info_list[2]
                if input_phone.isdigit() and len(input_phone) == 11:
                    with open("staff_info", "r") as f_tel:
                        for line in f_tel:
                            list_line = line.strip().split(",")
                            if list_line[3] == input_phone:
                                token = True
                    if token:
                        print("\033[1;31m 已存在相同电话 \033[0m!")
                        return
                    else:
                        break
                else:
                    print("电话是11位数字")
                    return
            input_job = insert_info_list[3]

            while True:
                input_date = insert_info_list[4]
                if is_valid_date(input_date):
                    break
                else:
                    print("日期格式错误")
                    return

            with open("staff_info", "r") as f_r, open("staff_info_backup", "w") as f_w:
                id = 1
                for line in f_r:  # 备份老文件
                    id += 1
                    f_w.write(line)
            with open("staff_info", "a") as f_new:
                f_new.write("%s,%s,%s,%s,%s,%s\n" \
                            % (id, input_name, input_age, input_phone, input_job, input_date))
            print("已添加")
        else:
            print("没有这个表")
    else:
        print("格式错误")

def delete():
    token = 0
    for line in input_list:
        token += 1
    if token < 5:
        print("格式错误")
    else:
        if input_list[1] == "from" and input_list[3] == "where":
            if input_list[2] == "staff_table":
                with open("staff_info", "r") as f, open("staff_info_backup", "w") as f_w:
                    for line in f:  # 备份老文件
                        f_w.write(line)
                id_list = []
                token = False
                for line in input_command:#迭代每一个字符，把等于号后面的数字提取出来
                    if line == "=":
                        token = True
                    if token:
                        id_list.append(line)
                input_id = "".join(id_list[1:]).strip()
                if input_id.isdigit():
                    token = True  # 设置一个标志位用于标识需要删除的行
                    token2 = False # 设置一个标志位用于识别是否有需要删除的那一行
                    with open("staff_info_backup", "r") as f_old, open("staff_info", "w") as f_new:
                        for line in f_old:
                            if line.startswith(input_id + ","):
                                token = False  # 当输入的id号等于这一行的开头数字则标记成false
                                token2 = True
                                continue
                            token = True  # 其余部分再标记成True
                            if token: #除了删除的这一行，如果id大于输入的id，那么在写入时全部减1
                                list_line = line.strip().split(",")
                                id = list_line[0]
                                if int(id) > int(input_id):
                                    list_line[0] = str(int(id) - 1)
                                w_into = ",".join(list_line)
                                f_new.write(w_into + "\n")
                    if token2:
                        print("删除成功")
                    else:
                        print("不存在该ID")
                else:
                    print("id是一个数字")
            else:
                print("没有这个表")
        else:
            print("格式错误")

def update():
    token = 0
    for line in input_list:
        token += 1
    if token < 5:
        print("格式错误")
    else:
#################################################################
#以update、set、where为关键词，提取出关键词后面的内容
        input_result_list_all = ["staff_id", "name", "age", "phone", "dept", "enroll_date"]
        update_dic = {
            "update":"",
            "set":"",
            "where":"",
        }
        token = 0
        update_list = []
        set_list = []
        where_list = []
        for line in input_list:
            if line == "update":
                token = 1
            elif line == "set":
                token = 2
            elif line == "where":
                token = 3
            if token == 1:
                update_list.append(line)
            elif token == 2:
                set_list.append(line)
            elif token == 3:
                where_list.append(line)

        update_list = update_list[1:]
        set_list = set_list[1:]
        where_list = where_list[1:]

        str_update = "".join(update_list)
        if str_update == "staff_table":
#################################################################
#把staff_info的内容提取成字典
            if not where_list == [] or set_list == []:

                with open("staff_info", "r") as f:
                    count = 0
                    token2 = True
                    for line in f:
                        list_line = line.strip().split(",")
                        info_dic = {
                            "staff_id": int(list_line[0]),
                            "name": list_line[1],
                            "age": int(list_line[2]),
                            "phone": list_line[3],
                            "dept": list_line[4],
                            "enroll_date": list_line[5],
                        }

#################################################################
# 分离where后面的字符串
                        str_where = "".join(where_list)
                        token = True
                        where_list_1 = []
                        where_list_2 = []
                        where_list_3 = []
                        where_list_4 = []
                        for line in str_where:
                            if line == "=" or line == ">" or line == "<":
                                token = False
                            if token:
                                where_list_1.append(line)
                                where_str1 = "".join(where_list_1) #where_str1是符号前的部分
                            else:
                                where_list_2.append(line)
                                where_str2 = "".join(where_list_2)
                        token2 = False
                        for line in where_str2:
                            if line == "=" or line == ">" or line == "<":
                                token2 = True
                            else:
                                token2 = False
                            if token2:
                                where_list_3.append(line)
                                where_str2 = "".join(where_list_3) #where_str2是符号
                            else:
                                where_list_4.append(line)
                                where_str3 = "".join(where_list_4).strip('"').strip("'") #where_str3是符号后的部分

#################################################################
#分离set后面的字符串
                        str_set = "".join(set_list)
                        set_list1 = []
                        set_list2 = []
                        set_token1 = True
                        for line in str_set:
                            if line == "=":
                                set_token1 = False
                            if set_token1:
                                set_list1.append(line)
                            else:
                                set_list2.append(line)
                        set_str1 = "".join(set_list1)
                        set_str2 = "".join(set_list2[1:]).strip('"').strip("'")

#################################################################
#通过where找到位置然后执行修改

                if where_str1 in input_result_list_all and set_str1 in input_result_list_all:
                    with open("staff_info", "r") as f_r, open("staff_info_backup", "w") as f_w:
                        id = 1
                        for line in f_r:  # 备份老文件
                            id += 1
                            f_w.write(line)
                    tag = True
                    with open("staff_info_backup", "r") as f_old , open("staff_info", "w") as f_new:
                        tag = False
                        for line in f_old:
                            list_line2 = line.strip().split(",")
                            info_dic2 = {
                                "staff_id": int(list_line2[0]),
                                "name": list_line2[1],
                                "age": int(list_line2[2]),
                                "phone": list_line2[3],
                                "dept": list_line2[4],
                                "enroll_date": list_line2[5],
                            }

                            if where_str2 == "=":#where的符号是等号
                                if where_str3.isdigit():#where的内容是数字

                                    if str(info_dic2.get(where_str1)) == where_str3:#where的内容等于字典里的内容
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n"\
                                               % (str(info_dic2["staff_id"]),\
                                                  info_dic2["name"],\
                                                  str(info_dic2["age"]),\
                                                  info_dic2["phone"],\
                                                  info_dic2["dept"],\
                                                  info_dic2["enroll_date"],\
                                                  )

                                else:#where的符号是等号，where的内容不是数字

                                    if str(str(info_dic2.get(where_str1).lower().replace(" ",""))) == where_str3:
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n" \
                                               % (str(info_dic2["staff_id"]), \
                                                  info_dic2["name"], \
                                                  str(info_dic2["age"]), \
                                                  info_dic2["phone"], \
                                                  info_dic2["dept"], \
                                                  info_dic2["enroll_date"], \
                                                  )
                            if where_str2 == ">":
                                if where_str3.isdigit():
                                    if info_dic2.get(where_str1) > int(where_str3):
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n" \
                                               % (str(info_dic2["staff_id"]), \
                                                  info_dic2["name"], \
                                                  str(info_dic2["age"]), \
                                                  info_dic2["phone"], \
                                                  info_dic2["dept"], \
                                                  info_dic2["enroll_date"], \
                                                  )
                            if where_str2 == "<":
                                if where_str3.isdigit():
                                    if info_dic2.get(where_str1) < int(where_str3):
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n" \
                                               % (str(info_dic2["staff_id"]), \
                                                  info_dic2["name"], \
                                                  str(info_dic2["age"]), \
                                                  info_dic2["phone"], \
                                                  info_dic2["dept"], \
                                                  info_dic2["enroll_date"], \
                                                  )
                            if where_str2 == ">=":
                                if where_str3.isdigit():
                                    if info_dic2.get(where_str1) >= int(where_str3):
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n" \
                                               % (str(info_dic2["staff_id"]), \
                                                  info_dic2["name"], \
                                                  str(info_dic2["age"]), \
                                                  info_dic2["phone"], \
                                                  info_dic2["dept"], \
                                                  info_dic2["enroll_date"], \
                                                  )
                            if where_str2 == "<=":
                                if where_str3.isdigit():
                                    if info_dic2.get(where_str1) <= int(where_str3):
                                        info_dic2[set_str1] = set_str2

                                        line = "%s,%s,%s,%s,%s,%s\n" \
                                               % (str(info_dic2["staff_id"]), \
                                                  info_dic2["name"], \
                                                  str(info_dic2["age"]), \
                                                  info_dic2["phone"], \
                                                  info_dic2["dept"], \
                                                  info_dic2["enroll_date"], \
                                                  )
#################################################################
# 对修改后的内容格式做一个检验

                            check_list = line.strip().split(",")

                            if not (check_list[2].isdigit() and len(check_list[2]) == 2) :
                                tag = True
                                print("年龄格式错误")
                                break
                            elif not (check_list[3].isdigit() and len(check_list[3]) == 11):
                                tag = True
                                print("电话格式错误")
                                break

                            elif not is_valid_date(check_list[5]):
                                tag = True
                                print("日期格式错误")
                                break
                            else:
                                f_new.write(line)
                    if tag:#检验不通过的话把老文件重新写会去
                        with open("staff_info_backup", "r") as f_old, open("staff_info", "w") as f_new:
                                for line2 in f_old:
                                    f_new.write(line2)
                    else:
                        print("已完成操作")


                else:
                    print("菜单名称不存在")
            else:
                print("命令格式错误")
        else:
            print("输入内容无效")

def select():
    token = 0
    for line in input_list:
        token += 1
    if token < 4:
        print("格式错误")
    else:
        input_result_list_all = ["staff_id", "name", "age", "phone", "dept", "enroll_date"]
        if input_list[2] == "from" and input_list[-4] == "where" or input_list[-4] == "select":
            if input_list[3] == "staff_table":
                input_condition = input_list[-3]  # 条件是列表的倒数第三项
                input_symbol = input_list[-2]  # 符号是列表的倒数第二项
                input_condtent = input_list[-1].strip('"')  # 内容是列表的最后一项
                input_result = input_list[1]  # 结果是列表的第二项
                if input_result == "*":  # 结果添加到input_result_list，如果结果是*，则全部添加
                    input_result_list = input_result_list_all
                else:
                    input_result_list = input_result.split(",")

                a = set(input_result_list)
                b = set(input_result_list_all)
                if not a <= b:#判断select的内容是否在指定的范围内
                    print(a)
                    print(b)
                    print("条件不存在")
                    return

                with open("staff_info", "r") as f:
                    count = 0
                    token2 = True
                    for line in f:
                        list_line = line.strip().split(",")
                        info_dic = {
                            "staff_id": int(list_line[0]),
                            "name": list_line[1],
                            "age": int(list_line[2]),
                            "phone": list_line[3],
                            "dept": list_line[4],
                            "enroll_date": list_line[5],
                        }

                        if input_symbol == "=" :
                            if input_condtent.isdigit():
                                #如果是数字那么不区分大小写
                                if str(info_dic.get(input_condition)) == input_condtent:
                                    # 如果符号是等号，并且字典里，通过条件获取的内容，和输入的内容一致,打印输出
                                    tmp_list = []
                                    input_result_list_addSpace = []
                                    for line in input_result_list:
                                        tmp_list.append(str(info_dic.get(line)).ljust(15))
                                        input_result_list_addSpace.append(line.ljust(15))
                                    tmp_list = ("").join(tmp_list)
                                    input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                    if token2:  # 只打印一遍标题，打印完token2变成false
                                        print("以下是您需要的结果".center(15 * 5, "-"))
                                        print(input_result_list_addSpace)
                                        token2 = False
                                    print(tmp_list)
                                    count += 1
                                    continue
                            else:
                                if  str(info_dic.get(input_condition).lower()) == input_condtent:
                                    # 如果是不是数字，需要把输入的大写统一转换成小写
                                    tmp_list = []
                                    input_result_list_addSpace = []
                                    for line in input_result_list:
                                        tmp_list.append(str(info_dic.get(line)).ljust(15))
                                        input_result_list_addSpace.append(line.ljust(15))
                                    tmp_list = ("").join(tmp_list)
                                    input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                    if token2:  # 只打印一遍标题，打印完token2变成false
                                        print("以下是您需要的结果".center(15 * 5, "-"))
                                        print(input_result_list_addSpace)
                                        token2 = False
                                    print(tmp_list)
                                    count += 1
                                    continue
                        elif input_symbol == ">":
                            if input_condtent.isdigit():
                                if str(info_dic.get(input_condition)).isdigit():
                                    if info_dic.get(input_condition) > int(input_condtent):
                                        tmp_list = []
                                        input_result_list_addSpace = []
                                        for line in input_result_list:
                                            tmp_list.append(str(info_dic.get(line)).ljust(15))
                                            input_result_list_addSpace.append(line.ljust(15))
                                        tmp_list = ("").join(tmp_list)
                                        input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                        if token2:  # 只打印一遍标题，打印完token2变成false
                                            print("以下是您需要的结果".center(15 * 5, "-"))
                                            print(input_result_list_addSpace)
                                            token2 = False
                                        print(tmp_list)
                                        count += 1
                                else:
                                    print("输入条件错误")
                                    break
                            else:
                                print("大于号后请输入数字")
                                break
                        elif input_symbol == "<":
                            if  input_condtent.isdigit():
                                if str(info_dic.get(input_condition)).isdigit():
                                    if info_dic.get(input_condition) < int(input_condtent):
                                        tmp_list = []
                                        input_result_list_addSpace = []
                                        for line in input_result_list:
                                            tmp_list.append(str(info_dic.get(line)).ljust(15))
                                            input_result_list_addSpace.append(line.ljust(15))
                                        tmp_list = ("").join(tmp_list)
                                        input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                        if token2:  # 只打印一遍标题，打印完token2变成false
                                            print("以下是您需要的结果".center(15 * 5, "-"))
                                            print(input_result_list_addSpace)
                                            token2 = False
                                        print(tmp_list)
                                        count += 1
                                else:
                                    print("输入条件错误")
                                    break
                            else:
                                print("小于号后请输入数字")
                                break
                        elif input_symbol == "like" :
                            if input_condtent.isdigit():
                                if str(input_condtent) in str(info_dic.get(input_condition)):
                                    tmp_list = []
                                    input_result_list_addSpace = []
                                    for line in input_result_list:
                                        tmp_list.append(str(info_dic.get(line)).ljust(15))
                                        input_result_list_addSpace.append(line.ljust(15))
                                    tmp_list = ("").join(tmp_list)
                                    input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                    if token2:  # 只打印一遍标题，打印完token2变成false
                                        print("以下是您需要的结果".center(15 * 5, "-"))
                                        print(input_result_list_addSpace)
                                        token2 = False
                                    print(tmp_list)
                                    count += 1
                            else:
                                if str(input_condtent) in str(info_dic.get(input_condition).lower())\
                                        and str(input_condtent):
                                    tmp_list = []
                                    input_result_list_addSpace = []
                                    for line in input_result_list:
                                        tmp_list.append(str(info_dic.get(line)).ljust(15))
                                        input_result_list_addSpace.append(line.ljust(15))
                                    tmp_list = ("").join(tmp_list)
                                    input_result_list_addSpace = (("").join(input_result_list_addSpace))
                                    if token2:  # 只打印一遍标题，打印完token2变成false
                                        print("以下是您需要的结果".center(15 * 5, "-"))
                                        print(input_result_list_addSpace)
                                        token2 = False
                                    print(tmp_list)
                                    count += 1
                        elif input_condtent == "staff_table":
                            tmp_list = []
                            input_result_list_addSpace = []
                            for line in input_result_list:
                                tmp_list.append(str(info_dic.get(line)).ljust(15))
                                input_result_list_addSpace.append(line.ljust(15))
                            tmp_list = ("").join(tmp_list)
                            input_result_list_addSpace = (("").join(input_result_list_addSpace))
                            if token2:#只打印一遍标题，打印完token2变成false
                                print("以下是您需要的结果".center(15*5,"-"))
                                print(input_result_list_addSpace)
                                token2 = False
                            print(tmp_list)
                            count += 1

                    print(">>>一共产生了\033[1;31m%s\033[0m条数据" % str(count))
                    print(">>>>>>")
            else:
                print("没有这个表")
        else:
            print("格式错误")

if __name__ == '__main__':
    while True:
        input_command = input("输入命令：").strip()
        if input_command == "q":
            exit()
        input_list = input_command.split(" ")  # 把输入的语句用空格间隔成一个列表
        command = input_list[0].lower()
        command_list = ["select", "insert", "delete", "update",]#"SELECT", "INSERT", "DELETE", "UPDATE"]
        if command in command_list:
            if command == "select" or command == "update":#因为查询和修改时需要区分大小写所以统一改成小写
                input_command = input_command.lower()
                input_list_tmp = []
                for line in input_list:#将input_list列表里的值都改成小写
                    line = line.lower()
                    input_list_tmp.append(line)
                input_list = input_list_tmp
            exec(command + "()")

        else:
            print("格式错误")