#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
coder is main file
"""
import json
from readcrd import ReadCRD
from query_coder import QueryCoder
from insert_coder import InsertCoder
from interface_coder import InterfaceCoder

class Coder(ReadCRD):
    def __init__(self,database,submodels,output,templates):
        super(Coder, self).__init__(database,submodel)
        self.output = output
        self.templates = templates
        self.query_coder = QueryCoder(database,submodel)
        self.insert_coder = InsertCoder(database,submodel)

    '''
    生成urls.py
    '''
    def urls_coder(self):
        file_string = ''
        file_string += ('urlpatterns = [\n')
        file_string += ('   path( \'qu{}/\', views.query_{}),\n'.format(self.submodel[0:3],self.submodel))
        file_string += ('   path( \'in{}/\', views.insert_{}),\n'.format(self.submodel[0:3],self.submodel))
        file_string += (']\n')
        return file_string
    
    ''' 
    load temple code file
    '''
    def src_coder(self):
        #print(self.query_config)
        views_file_name = "{}/{}/views.py".format(self.output,submodel)
        urls_file_name = "{}/{}/urls.py".format(self.output,submodel)

        # write to views.py
        with open(self.templates["views"],'r') as f:
             temple_code = ''
             lines = f.readlines()
        for line in lines:
            if "query_submodel" in line: 
                line = line.replace("query_submodel","query_{}".format(submodel))
            if "insert_submodel" in line: 
                line = line.replace("insert_submodel","insert_{}".format(submodel))
            temple_code += line
        # query code
        query_code = self.query_coder.query_coder()
        insert_code = self.insert_coder.insert_coder()
        final_code = temple_code + query_code + insert_code
        with open(views_file_name ,'w') as file_object:
            file_object.write(final_code)


        # write to urls.py
        with open(self.templates["urls"],'r') as f:
            temple_code = f.read()
        urls_code = self.urls_coder()
        final_code = temple_code + urls_code
        with open(urls_file_name,'w') as file_object:
            file_object.write(final_code)


if __name__ == "__main__":
    src_out_path = "../"
    config_path = "crd/"
    database = "cec"
    submodels = [
        "customer",
       # "finance",
       # "cash"
    ]
    template_files = {
        "views":'templates/views.py',
        "urls":'templates/urls.py',
        "interface":'templates/interface.md'
    }

    for submodel in submodels:
        I_coder = Coder(database,submodel,src_out_path,template_files)
        I_coder.src_coder()

        interface_coder = InterfaceCoder(database,submodel)
        interface_coder.interface_coder(src_out_path,template_files)   
