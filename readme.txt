1、本程序有个文件
	1、程序代码文件
	2、员工信息数据文件
	3、程序流程图
2、本程序可以对员工信息数据进行查询，增加，修改，删除等操作，支持以下语法：
	本系统支持以下查询语法:
   	 1、find name,age from staff_table where age > 22
    	 2、find * from staff_table where dept = "IT"
    	 3、find * from staff_table where enroll_date like "2013"
    	本系统支持以下修改语法:
   	 1、update staff_table set dept="Market" where  dept = "IT"
     	 2、update staff_table set age=25 where  name = "Alex Li"
    	本系统支持以下增加语法：
    	 1、add staff_table Alex Li,25,134435344,IT,2015‐10‐29
        本系统支持以下删除语法：
         1、del from staff where id=3
	
3、要对数据进行操作需要输入管理员账号
	用户名：admin
	密码：123456