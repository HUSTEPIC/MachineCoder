from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from cmdb.models import CustomerBase,CustomerCredit
from django.db import connection
from django.db import transaction
import sys
# Create your views here.
def query_submodel(request):
    if request.method == 'GET':
        queryDict = request.GET
    elif request.method == 'POST':
        queryDict = request.POST

    sql_code_final = query_by(queryDict)

    page = int(queryDict.get('page',0))
    limit = int(queryDict.get('limit',0))
    layui_json = query_by_sql_code(sql_code_final,page,limit)    
    
    return JsonResponse(layui_json, safe=False)
    #return HttpResponse(JsonResponse(layui_json), content_type="application/json")

# insert data
def insert_submodel(request):
    if request.method == 'GET':
        insert_values_post = request.GET
    elif request.method == 'POST':
        insert_values_post = request.POST

    sql_final = insert_sql(insert_values_post)
    with connection.cursor() as cursor:
        cursor.execute(sql_final)

    response = HttpResponse()
    response.content = 0 #val
    response.status_code = 200

    return response
    
def query_by_sql_code(sql_code,page,limit):
    with connection.cursor() as cursor:
        cursor.execute(sql_code)
        desc = cursor.description
        data = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
#    print(data)
    if page >=1 and limit>=1:
       start = (page-1)*limit
       end = page*limit
       return_data = data[start:end]
    else:
       return_data = data
    layui_json = {
    "code": 0,
    "msg": "",
    "count": sys.getsizeof(return_data),
    "data": return_data
    }

    return layui_json
