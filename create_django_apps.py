import json
import os

project_config_path = 'crd/app_config.json'
def read_app_config():
    with open(project_config_path,'r') as f:
         app_config = f.read()
         config_dict = json.loads(app_config)
    framework = config_dict['framework']
    app_name = config_dict['app_name']
    sub_models = config_dict['sub_models']
    datasets = config_dict['datasets']
    print(datasets['default'])
    return (framework,app_name,sub_models,datasets)

def create_app():
    framework,app_name,sub_models,datasets= read_app_config()
    if framework == "django":
       # create project
       if not os.access(app_name,os.F_OK):
          os.system('django-admin startproject {}'.format(app_name))
       os.chdir(app_name)
       # create app 
       for sub_model in sub_models:
          os.system('python manage.py startapp {}'.format(sub_model))
       # config datasets
       os.chdir(app_name)
       


if __name__ == "__main__":
    read_app_config()
#    create_app()