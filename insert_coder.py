from readcrd import ReadCRD


class InsertCoder(ReadCRD):
   def __init__(self,database,submodel):
       super(InsertCoder,self).__init__(database,submodel)
       self.insert_table = self.insert_config['INTO']          
       self.insert_head = self.read_table_column_name(self.insert_table)
       self.get_insert_sql()
       #self.insert_head = self.insert_config['HEAD']         # 表头

   '''
   生成插入SQL语句
   '''
   def get_insert_sql(self):
       code = "INSERT INTO {} (".format(self.insert_table)
       for column_index,column in enumerate(self.insert_head):
           if column_index < len(self.insert_head)-1 :
              code += "{}, ".format(column)
           else:
              code += "{}) ".format(column)
       self.sql_base = code
       #print(self.sql_base)
       #self.value_code = self.get_default_insert_value_by_type(insert_table,insert_head)
       #return (sql_base,value_code)

       
   def get_default_insert_value_by_type(self,column):
# 
           column_type = self.get_type_of_column("{}.{}".format(self.insert_table,column))
           if 'enum' in column_type: 
              code = "\'{}\'".format(column_type.split('\'')[1])
           elif 'tinyint'  in column_type or 'decimal' in column_type \
                or 'int' in column_type:
              code = "\'0\'"
           elif 'date' in column_type:
              code = "\'2008-08-08\'"
           elif 'double' in column_type:
              code = "\'0\'"
           else:
              code = "\'\'"
           return code

#           if column_index < len(self.insert_head)-1 :
#              code += ","
#           value_code += code
#       value_code += ")"
#       return value_code 

   '''
   增加记录SQL代码
   '''
   def insert_coder(self):
       insert_code = ""
       insert_code += ('def insert_sql(insert_values_post):\n')
       insert_code += ('    sql_base = \'\'\'{}\'\'\'\n'.format(self.sql_base))

       for _,column in enumerate(self.insert_head):
           insert_code += ('    {0} = insert_values_post.get(\'{0}\',{1}) \n'.format(column,self.get_default_insert_value_by_type(column)))
       insert_code += ('    value_code = \'\'\'VALUES (')
       for column_index,column in enumerate(self.insert_head):
           if column_index < len(self.insert_head)-1:
              insert_code += ("\'{%s}\',"%(column_index))
           elif column_index == len(self.insert_head) -1:
              insert_code += ("\'{%s}\')\'\'\'.format("%(column_index))
       for column_index,column in enumerate(self.insert_head):
           if column_index < len(self.insert_head)-1:
              insert_code += ('{},'.format(column))
           elif column_index == len(self.insert_head) -1:
              insert_code += ('{})\n'.format(column))
       insert_code += ('    sql_final = sql_base + value_code\n')
       insert_code += ('    return sql_final \n')
#       print(insert_code)
       return insert_code

   def get_interface_test_code(self):
       interface_test = 'curl http://localhost:8080/{}/in{}/ -X POST -i -d '.format(self.submodel,self.submodel[0:3])
       for column_index,column in enumerate(self.insert_head):
           if column_index < len(self.insert_head)-1:
              interface_test += ('{}={}\&'.format(column,self.get_default_insert_value_by_type(column)))
           elif column_index == len(self.insert_head) -1:
              interface_test += ('{}={}'.format(column,self.get_default_insert_value_by_type(column)))
       print(interface_test)
       return interface_test


if __name__ == "__main__":
   submodels = ['customer']
   insert_coder = InsertCoder('cec',submodels[0])
#   insert_coder.insert_coder()
   insert_coder.get_interface_test_code()
