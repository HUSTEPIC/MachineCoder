#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
coder is main file

"""
import json

database_name = "cec"

'''
读取子模块的需求文档
'''
def read_submodels_config(submodel_config_path):
    with open(submodel_config_path,'r') as f:
         submodel_config = f.read()
         config_dict = json.loads(submodel_config)
    # 查询需求
    query = config_dict['QUERY']
    return (query)



'''
读取数据库的表列名
'''
def read_table_column_name(table_name):
    columns = []
    table_path = "crd/{}.txt/{}_table_{}.txt".format(database_name,database_name,table_name)
    with open(table_path,'r') as table_file:
        column_dic = {}
        table = table_file.readlines()
        for row_index,row in enumerate(table):
            if row_index > 5:
               column_dic['column_name'] = row.split("|")[1]
               column_dic['column_type'] = row.split("|")[2]
               columns.append(column_dic)
    return columns

'''
读取数据库表的表列的类型名
'''
def get_type_of_column(column_name):
    table_name = column_name.split('.')[0]
    column = column_name.split('.')[1]
    table_path = "crd/{}.txt/{}_table_{}.txt".format(database_name,database_name,table_name)
    with open(table_path,'r') as table_file:
        column_dic = {}
        table = table_file.readlines()
        for row_index,row in enumerate(table):
            if row_index > 5:
               column_dic[row.split("|")[1]] = row.split("|")[2]
    return column_dic[column]

"""
no condiction to query
"""
def code_query_no_cond(return_columns,table_name):
    code = "SELECT "
    for column_index,column in enumerate(return_columns):
        if column_index < len(return_columns)-1:
           code += "{}, ".format(column)
        else:
           code += "{} ".format(column)
    code += "FROM {}".format(table_name)
    print(code)
    return code

'''
生成条件查询SQL语句
'''
def code_query_by(query_config):
    ui_head = query_config['HEAD']         # 表头
    from_tables = query_config['FROM']      # 数据库表
    conditions = query_config['CONDITION']  # 查询条件
    order = query_config['ORDER']          # 显示顺序
    code = "SELECT "
    for column_index,column in enumerate(ui_head):
        if column_index < len(ui_head)-1 :
           code += "{}, ".format(column)
        else:
           code += "{} ".format(column)
    #print(ui_head,condition,from_table,order)
    for table_index,table in enumerate(from_tables):
        if table_index == 0:
           code += "FROM {} ".format(table)
        else:
           code += "LEFT JOIN {} ON {}.{} = {} ".format(table.split('.')[0],from_tables[0],table.split('.')[1],table)
    sql_base = code
    sql_condition = []
    for condition_index,condition in enumerate(conditions):
        if get_type_of_column(condition) == 'date':
           condition_code = "BETWEEN '{{}}' AND '{{}}' \'\'\'.format({0}.split(',')[0],{0}.split(',')[1])".format(condition.split('.')[1])
        elif 'double' in get_type_of_column(condition) or 'decimal' in get_type_of_column(condition) \
          or 'tinyint' in get_type_of_column(condition) or 'varchar' in get_type_of_column(condition) \
          or 'int' in get_type_of_column(condition):
           condition_code = "= {{}} \'\'\'.format({})".format(condition.split('.')[1])
        #elif  'varchar' in get_type_of_column(condition):
        else:
           condition_code = "= '{{}}' \'\'\'.format({})".format(condition.split('.')[1])
       
#        if condition_index == 0:
#           code = "WHERE {} {} ".format(condition,condition_code)
#        else:
#           code = "AND {} {} ".format(condition,condition_code)
        code = "{} {}".format(condition,condition_code)
        sql_condition.append(code)
    sql_order = "ORDER BY {} {}".format(order[1],order[0])
        
    print(sql_base)
    print(sql_condition)
    print(sql_order)
    return sql_base,sql_condition,sql_order

'''
根据模板生成views.py的代码
'''
def query_coder(submodel_config_path):
    file_name = 'views.py'
    query_config = read_submodels_config(submodel_config_path)
    sql_base,sql_conditions,sql_order = code_query_by(query_config)
    with open(file_name,'w') as file_object:
        file_object.write('def query_by(queryDict):\n')
        file_object.write('    sql_base = \'\'\'{}\'\'\'\n'.format(sql_base))
        file_object.write('    sql_end= \'\'\'{}\'\'\'\n'.format(sql_order))
        file_object.write('    condition_index = 0\n')
        file_object.write('    sql_conditions = \'\'\n')
        # condition 
        for index, sql_condition in enumerate(query_config['CONDITION']):
            file_object.write('    {} = queryDict.get(\'{}\',\'\') \n'.format(sql_condition.split('.')[1],sql_condition.split('.')[1]))
            file_object.write('    if {}: \n'.format(sql_condition.split('.')[1]))
            file_object.write('       condition_index += 1\n')
            file_object.write('       if condition_index == 1:\n')
            file_object.write('          sql_conditions = \'\'\'WHERE {}\n'.format(sql_conditions[index],sql_condition.split('.')[1]))
            file_object.write('       else:\n')
            file_object.write('          sql_conditions += \'\'\'AND {}\n'.format(sql_conditions[index],sql_condition.split('.')[1]))
            
        file_object.write('    sql_final = sql_base + sql_conditions + sql_end\n')
        file_object.write('    return sql_final \n')
    with open(file_name,'r') as f:
        query_code = f.read()        
    return query_code

''' 
load temple code file
'''
def write_to_temple(temple_file,submodel_config_path):
    file_name = 'views.py'
    with open(temple_file,'r') as f:
         temple_code = f.read()

    query_code = query_coder(submodel_config_path)
    final_code = temple_code + query_code 

    with open(file_name,'w') as file_object:
        file_object.write(final_code)
    return (final_code)

if __name__ == __name__:
    table_name = "come_money"
    column_name = "come_no"
    return_columns=["come_money.come_no","come_money.come_money","come_money.come_date"]
    temple_file = 'temple_code/query_temple_code.py'
#    submodel_config_path = "crd/cash.json"
    submodel_config_path = "crd/finance.json"
#    read_table_column_name('come_money')
#    code_query_no_cond(return_columns,table_name)
    write_to_temple(temple_file,submodel_config_path)