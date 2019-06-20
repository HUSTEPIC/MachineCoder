from readcrd import ReadCRD
from insert_coder import InsertCoder

class InterfaceCoder(ReadCRD):
      def __init__(self,database,submodel):
          super(InterfaceCoder,self).__init__(database,submodel)
          self.database_name = database
          self.submodel = submodel
      
      ''' 
      生成接口文档
      '''
      def interface_coder(self,interface_out_path,template_files):
          readcrd = ReadCRD('cec',self.submodel)
          with open(template_files["interface"],'r') as f:
               interface_string = f.read()
               interface_file_name = "{}/interface.md".format(interface_out_path)
      #        example = []
      #        for condition in query_config["CONDITION"]:
      #            example.append("curl http://localhost:8080/{}/{}/ -X POST -i -d {} =  value ")
               interface_string += "| {}/ | qu{}/ | {} | \n".format(self.submodel,self.submodel[0:3],readcrd.query_config)
          insert_coder = InsertCoder(self.database_name,self.submodel)
          insert_interface_test_string = insert_coder.get_interface_test_code()
              # write to interface.md
          with open(interface_file_name,'w') as file_object:
               file_object.write(interface_string)
               file_object.write(insert_interface_test_string)

