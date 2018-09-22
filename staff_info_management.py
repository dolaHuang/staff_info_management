from tabulate import tabulate
from prettytable import PrettyTable


# 定义装饰器，功能：登录
def login(func):
    def inner():
        global flag     # 声明全局变量
        if flag:
            func()
        else:
            username_def = 'admin'
            password_def = '123456'
            print("请先登录管理员账户！")
            username = input("用户名: ")
            password = input("密码:")
            if username == username_def and password == password_def:
                print("Welcome！", username)
                flag = True
                func()
            else:
                exit("用户名或者密码错误，登录失败!")
    return inner


# 定义函数，功能：更新员工信息将修改、增加、删除的内容更新到列表和字典里
def save_info(save_list):
    global staff_list, staff_dic
    staff_list = save_list
    staff_dic = {}
    for j_save in STAFF_COLUMN:
        staff_dic[j_save] = []
    for i_save in staff_list:
        for index_save, value_save in enumerate(STAFF_COLUMN):
            staff_dic[value_save].append(i_save[index_save])


# 定义函数，功能：显示影响的条数
def line_num(list_result, str_func):
    len_list_result = len(list_result)
    print('\033[1;31m本次操作共%s%s条信息\033[0m' % (str_func, len_list_result))


# 定义函数，功能：各个OP函数中的用来提取数据的代码块
def func_op_date(i_clause, clause_set):
    record = []
    for j_clause in STAFF_COLUMN:
        record.append(staff_dic[j_clause][i_clause])
    clause_set.append(record)


# 定义函数，功能：检测到是 > 后，处理数据，提取需要的数据
def op_gt(condition, val):
    clause_set = []
    for i_clause, v_clause in enumerate(staff_dic[condition.strip()]):
        val = val.strip()
        if val.isdigit():
            if float(v_clause) > float(val):
                func_op_date(i_clause, clause_set)
        else:
            print('\033[1;31m语法错误(<,>后面必须是数字)\033[0m')
            break
    return clause_set


# 定义函数，功能：检测到是 < 后，处理数据，提取需要的数据
def op_lt(condition, val):
    clause_set = []
    for i_clause, v_clause in enumerate(staff_dic[condition.strip()]):
        if val.isdigit():
            if float(v_clause) < float(val):
                func_op_date(i_clause, clause_set)
        else:
            print('\033[1;31m语法错误(<,>后面必须是数字)\033[0m')
            break
    return clause_set


# 定义函数，功能：检测到是 = 后，处理数据，提取需要的数据
def op_eq(condition, val):
    clause_set = []
    for i_clause, v_clause in enumerate(staff_dic[condition.strip()]):
        val = val.strip()
        if val.isdigit():
            if float(v_clause) == float(val):
                func_op_date(i_clause, clause_set)
        else:
            val = val.strip('\'')
            val = val.strip('\"')
            if v_clause == val:
                func_op_date(i_clause, clause_set)
    return clause_set


# 定义函数，功能：检测到是 like 后，处理数据，提取需要的数据
def op_like(condition, val):
    clause_set = []
    val = val.strip()
    val = val.strip('\'')
    val = val.strip('\"')
    for i_clause, v_clause in enumerate(staff_dic[condition.strip()]):
        if val in v_clause:
            func_op_date(i_clause, clause_set)
    return clause_set


# 定义函数，功能：分析where语句
def syntax_where(clause):
    operators = {
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        'like': op_like
    }
    for key_op in operators:
        if key_op in clause:
            condition, val = clause.split(key_op)
            for COLUMN in STAFF_COLUMN:
                condition = condition.strip()
                if condition == COLUMN:
                    op_func = operators[key_op]
                    op_set = op_func(condition, val)
                    return op_set
            else:
                print('\033[1;31m语法错误，找不到选项请尝试（staff_id, name, age, phone, dept, enroll_date)\033[0m')
                break
    else:
        print('\033[1;31m语法错误(<,>,=,like)\033[0m')


# 定义函数，功能：分析find
def syntax_find(clause_set, clause_left):
    find_set = []
    word_find = clause_left[1].split(',')
    if clause_left[1] == '*':  # 如果是* 就是个人信息的全部内容
        find_set = clause_set
        line_num(find_set, '查询')
        print(tabulate(find_set, headers=STAFF_COLUMN, tablefmt='gird'))
    elif len(clause_left[1]):
        for row_find in clause_set:
            find_record = []
            for word in word_find:
                if word in STAFF_COLUMN:
                    find_record.append(row_find[STAFF_COLUMN.index(word)])
                else:
                    print('\033[1;31m语法错误，找不到选项请尝试（staff_id, name, age, phone, dept, enroll_date)\033[0m')
                    break
            find_set.append(find_record)
        line_num(find_set, '查询')
        print(tabulate(find_set, headers=word_find, tablefmt='gird'))
    else:
        print('\033[1;31m语法错误(eg:find name,age from staff_table where age > 22）\033[0m')


# 定义函数，功能：分析update
def syntax_update(clause_set, clause_left):
    if clause_left[1] == 'staff_table' and clause_left[2] == 'set':  # 确保语法输入正确
        if '=' in clause_left[3]:   # 检查语法中的‘=’
            condition_update, val_update = clause_left[3].split('=')
            val_update = val_update.strip('\'')  # 如果语句中的关键字有引号，就去掉
            val_update = val_update.strip('\"')
            for row_update in clause_set:
                row_update[STAFF_COLUMN.index(condition_update)] = val_update  # 把获得的数据中的原值修改成语法设置的值
            line_num(clause_set, '修改')
            print(tabulate(clause_set, headers=STAFF_COLUMN, tablefmt='gird'))
            for index_row, val_row in enumerate(staff_list):  # 修改原列表数据中的员工信息
                for update_row in clause_set:
                        if update_row[0] == val_row[0]:
                            staff_list[index_row] = update_row
            save_info(staff_list)
        else:
            print('\033[1;31m语法错误(eg:update staff_table set age=25 where  name = "Alex Li")\033[0m')
    else:
        print('\033[1;31m语法错误(eg:update staff_table set age=25 where  name = "Alex Li")\033[0m')


# 定义函数，功能：分析del
def syntax_del(clause_set, clause_left):
    """
    :param clause_set: [['3', 'Rain Wang', '21', '13451054608', 'IT', '2017‐04‐01']]
    :param clause_left: ['del', 'from', 'staff_table']
    :return:
    """
    if len(clause_left) == 3:
        info_del = clause_set[0]
        for i_del, v_del in enumerate(staff_list):
            if v_del[0] == info_del[0]:
                staff_list.pop(i_del)   # 从列表中删除
                save_info(staff_list)
                print('\033[1;31m本次操作共删除1条员工信息\033[0m')
                add_table = PrettyTable(STAFF_COLUMN)
                add_table.add_row(info_del)
                print(add_table)
                break
    else:
        print('\033[1;31m语法错误(eg:del from staff_table where staff_id=3)\033[0m')


# 定义函数，功能：添加新员工信息
def syntax_add(cmd):
    if len(cmd.split()) >= 3:
        clause_add = cmd.split('staff_table')
        add_info = clause_add[1].split(',')
        add_id = int(staff_list[-1][0])+1
        add_info.insert(0, str(add_id))
        if len(add_info) == 6:
            if add_info[STAFF_COLUMN.index('phone')] in staff_dic['phone']:
                print('电话号码重复，无法添加')
            else:
                staff_list.append(add_info)
                print('添加成功')
                save_info(staff_list)
                add_table = PrettyTable(STAFF_COLUMN)
                add_table.add_row(add_info)
                print('\033[1;31m本次操作共添加1条员工信息\033[0m')
                print(add_table)
        else:
            print('\033[1;31m语法错误(eg:add staff_table Alex Li,25,134435344,IT,2015‐10‐29)\033[0m')
    else:
        print('\033[1;31m语法错误(eg:add staff_table Alex Li,25,134435344,IT,2015‐10‐29)\033[0m')


# 定义函数，功能：分析用户输入的语句
def syntax_parser(cmd):
    operators_left = {
        'find': syntax_find,
        'update': syntax_update,
        'del': syntax_del,
        'add': syntax_add
    }
    # 先判断用户的输入cmd 中是否以（find，update，add，del）开头
    if cmd.split()[0] in ('find', 'update', 'del'):
        if 'where' in cmd.split():
            left_part, right_part = cmd.split('where')
            where_set = syntax_where(right_part)    # 得到where处理的数据
            if where_set:
                clause_left = left_part.split()   # 根据语法的开头单词，调用相应函数
                for key_left in operators_left:
                    if key_left == clause_left[0]:
                        operators_left[key_left](where_set, clause_left)   # 调用函数来处理从where分析得到的数据
            else:
                print('\033[1;31m系统没有匹配的员工信息\n\033[0m')
        else:
            print('\033[1;31m语法错误(find,update,del,add......\\from staff_table where...)\033[0m')
    elif cmd.startswith('add'):
            operators_left['add'](cmd)
    else:
        print('\033[1;31m语法错误(find,update,del,add......\\from staff_table where...)\033[0m')


# 主函数
@login
def main():
    print(info)
    while True:
        cmd = input('请输入操作语法（输入q退出系统）》》').strip()
        if len(cmd.split()) < 1:
            print('\033[1;31m语法错误(find,update,del,add......\\from staff_table where...)\033[0m')
        elif cmd == 'q':   # 输入q 退出程序，并保存信息到文件里
            with open(STAFF_FILE, 'w', encoding='utf-8') as save_file:
                for list_row in staff_list:
                    file_row = ','.join(list_row) + '\n'
                    save_file.write(file_row)
            exit('程序已退出')
        else:
            syntax_parser(cmd)


info = '''
=*==*==*==*==*==*==*=员工信息管理系统==*==*==*==*==*==*==*==*=
本系统可以对系统内的员工信息进行增加、删除、查询、修改等操作
    查询语法:
    1、find name,age from staff_table where age > 22
    2、find * from staff_table where dept = IT
    3、find * from staff_table where enroll_date like "2013"
    修改语法:
    1、update staff_table set dept=Market where  dept = IT
    2、update staff_table set age=25 where  name = "Alex Li"
    增加语法：
    1、add staff_table Alex Li,25,134435344,IT,2015‐10‐29
    删除语法：
    1、del from staff_table where staff_id=3
=*==*==*==*==*==*==*==*==*==*==*==*==*==*==*==*==*==*==*==*=
'''
STAFF_FILE = 'staff_table.txt'
STAFF_COLUMN = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
staff_list = []
staff_dic = {}
flag = False

# 把文件数据转换成需要的字典格式
with open(STAFF_FILE, 'r', encoding='utf-8') as STAFF_INFO:
    for i, v in enumerate(STAFF_INFO):
        row = v.strip().split(',')
        staff_list.append(row)
for j in STAFF_COLUMN:
    staff_dic[j] = []
for i in staff_list:
    for index, value in enumerate(STAFF_COLUMN):
        staff_dic[value].append(i[index])


main()



