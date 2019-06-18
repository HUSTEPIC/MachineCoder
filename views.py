from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from cmdb.models import CustomerBase,CustomerCredit
from django.db import connection
from django.db import transaction
import sys
# Create your views here.
def queryCash(request):
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
def query_by(queryDict):
    sql_base = '''SELECT sale.customer_no, customer_credit.customer_name, sale.sale_no, sale_sub.contract_no, sale.sale_money, sale_sub.discount, sale_sub.sale_number, sale_sub.sale_date, sale_sub.check_account_code, sale_sub.invoice_no, sale_sub.invoice_date FROM sale LEFT JOIN sale_sub ON sale.sale_no = sale_sub.sale_no LEFT JOIN customer_credit ON sale.customer_no = customer_credit.customer_no '''
    sql_end= '''ORDER BY sale.sale_date DESC'''
    condition_index = 0
    sql_conditions = ''
    invoice = queryDict.get('invoice','') 
    if invoice: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.invoice = '{}' '''.format(invoice)
       else:
          sql_conditions += '''AND sale_sub.invoice = '{}' '''.format(invoice)
    is_dzd = queryDict.get('is_dzd','') 
    if is_dzd: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.is_dzd = {} '''.format(is_dzd)
       else:
          sql_conditions += '''AND sale_sub.is_dzd = {} '''.format(is_dzd)
    customer_no = queryDict.get('customer_no','') 
    if customer_no: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale.customer_no = {} '''.format(customer_no)
       else:
          sql_conditions += '''AND sale.customer_no = {} '''.format(customer_no)
    sale_no = queryDict.get('sale_no','') 
    if sale_no: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale.sale_no = {} '''.format(sale_no)
       else:
          sql_conditions += '''AND sale.sale_no = {} '''.format(sale_no)
    contract_no = queryDict.get('contract_no','') 
    if contract_no: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.contract_no = {} '''.format(contract_no)
       else:
          sql_conditions += '''AND sale_sub.contract_no = {} '''.format(contract_no)
    sale_date = queryDict.get('sale_date','') 
    if sale_date: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.sale_date BETWEEN '{}' AND '{}' '''.format(sale_date.split(',')[0],sale_date.split(',')[1])
       else:
          sql_conditions += '''AND sale_sub.sale_date BETWEEN '{}' AND '{}' '''.format(sale_date.split(',')[0],sale_date.split(',')[1])
    check_account_code = queryDict.get('check_account_code','') 
    if check_account_code: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.check_account_code = {} '''.format(check_account_code)
       else:
          sql_conditions += '''AND sale_sub.check_account_code = {} '''.format(check_account_code)
    invoice_no = queryDict.get('invoice_no','') 
    if invoice_no: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.invoice_no = {} '''.format(invoice_no)
       else:
          sql_conditions += '''AND sale_sub.invoice_no = {} '''.format(invoice_no)
    invoice_date = queryDict.get('invoice_date','') 
    if invoice_date: 
       condition_index += 1
       if condition_index == 1:
          sql_conditions = '''WHERE sale_sub.invoice_date BETWEEN '{}' AND '{}' '''.format(invoice_date.split(',')[0],invoice_date.split(',')[1])
       else:
          sql_conditions += '''AND sale_sub.invoice_date BETWEEN '{}' AND '{}' '''.format(invoice_date.split(',')[0],invoice_date.split(',')[1])
    sql_final = sql_base + sql_conditions + sql_end
    return sql_final 
