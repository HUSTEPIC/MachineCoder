from readcrd import  ReadCRD

class QueryCoder(ReadCRD):
   def __init__(self,database,submodel):
       super(QueryCoder,self).__init__(database,submodel)
       self.ui_head = self.query_config['HEAD']         # 表头
       self.from_tables = self.query_config['FROM']      # 数据库表
       self.conditions = self.query_config['CONDITION']  # 查询条件
       self.order = self.query_config['ORDER']          # 显示顺序
       self.get_query_sql()

   '''
   生成条件查询SQL语句
   '''
   def get_query_sql(self):
       code = "SELECT "
       for column_index,column in enumerate(self.ui_head):
           if column_index < len(self.ui_head)-1 :
              code += "{}, ".format(column)
           else:
              code += "{} ".format(column)
       for table_index,table in enumerate(self.from_tables):
           if table_index == 0:
              code += "FROM {} ".format(table)
           else:
              code += "LEFT JOIN {} ON {}.{} = {} ".format(table.split('.')[0],self.from_tables[0],table.split('.')[1],table)
       self.sql_base = code
       self.sql_conditions = []
       for _,condition in enumerate(self.conditions):
           if self.get_type_of_column(condition) == 'date':
              condition_code = "BETWEEN '{{}}' AND '{{}}' \'\'\'.format({0}.split(',')[0],{0}.split(',')[1])".format(condition.split('.')[1])
           elif 'double' in self.get_type_of_column(condition) or 'decimal' in self.get_type_of_column(condition) \
             or 'tinyint' in self.get_type_of_column(condition) or 'varchar' in self.get_type_of_column(condition) \
             or 'int' in self.get_type_of_column(condition):
              condition_code = "= {{}} \'\'\'.format({})".format(condition.split('.')[1])
           #elif  'varchar' in get_type_of_column(condition):
           else:
              condition_code = "= '{{}}' \'\'\'.format({})".format(condition.split('.')[1])
              
           code = "{} {}".format(condition,condition_code)
           self.sql_conditions.append(code)
       self.sql_order = "ORDER BY {} {}".format(self.order[1],self.order[0])
   
   '''
   根据模板生成views.py的代码
   '''
   def query_coder(self):
       query_code = ''
       query_code += ('def query_by(queryDict):\n')
       query_code += ('    sql_base = \'\'\'{}\'\'\'\n'.format(self.sql_base))
       query_code += ('    sql_end= \'\'\'{}\'\'\'\n'.format(self.sql_order))
       query_code += ('    condition_index = 0\n')
       query_code += ('    sql_conditions = \'\'\n')
       # condition 
       for index, condition in enumerate(self.conditions):
           query_code += ('    {} = queryDict.get(\'{}\',\'\') \n'.format(condition.split('.')[1],condition.split('.')[1]))
           query_code += ('    if {}: \n'.format(condition.split('.')[1]))
           query_code += ('       condition_index += 1\n')
           query_code += ('       if condition_index == 1:\n')
           query_code += ('          sql_conditions = \'\'\'WHERE {}\n'.format(self.sql_conditions[index]))#,sql_condition.split('.')[1]))
           query_code += ('       else:\n')
           query_code += ('          sql_conditions += \'\'\'AND {}\n'.format(self.sql_conditions[index]))#,sql_condition.split('.')[1]))
           
       query_code += ('    sql_final = sql_base + sql_conditions + sql_end\n')
       query_code += ('    return sql_final \n')
       #print(query_code)  
       return query_code

if __name__ == "__main__":
    submodels = [
        "customer",
#        "finance",
#        "cash"
    ]
    query_coder = QueryCoder('cec',submodels[0])
    query_coder.query_coder()