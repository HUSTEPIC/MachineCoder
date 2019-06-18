#!/bin/bash

cat crd/requirements.crd | while read LINE  
do
    echo $LINE 
done

# mkdir src
# django-admin startproject erp_backend
# python manage.py startapp 