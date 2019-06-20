import json

class ReadCRD:
    '''
    读取子模块的代码需求文档(code requirement documents)
    '''
    def __init__(self,database,submodel):
        self.database_name = database
        self.submodel = submodel
        
        submodel_config_path = "crd/{}.json".format(submodel)
        with open(submodel_config_path,'r') as f:
            submodel_config = f.read()
            self.config_dict = json.loads(submodel_config)
        
        # 查询需求
        self.query_config = self.config_dict['QUERY']
        # 插入需求
        self.insert_config = self.config_dict['INSERT']

    '''
    读取数据库表的表列的类型名
    '''
    def get_type_of_column(self,column_name):
        table_name = column_name.split('.')[0]
        column = column_name.split('.')[1]
        table_path = "crd/{0}.txt/{0}_table_{1}.txt".format(self.database_name,table_name)
        with open(table_path,'r') as table_file:
            column_dic = {}
            table = table_file.readlines()
            for row_index,row in enumerate(table):
                if row_index > 5:
                   column_dic[row.split("|")[1]] = row.split("|")[2]
    #    print(column_dic)
        return column_dic[column]

    '''
    读取数据库的表列名
    '''
    def read_table_column_name(self,table_name):
        columns = []
        table_path = "crd/{0}.txt/{0}_table_{1}.txt".format(self.database_name,table_name)
        with open(table_path,'r') as table_file:
            table = table_file.readlines()
            for row_index,row in enumerate(table):
                if row_index > 5:
                   column = row.split("|")[1]
                   columns.append(column)
        return columns


