import datetime
import django
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.db import OperationalError, connections
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
import json
import os
import pandas as pd
import numpy as np
from storesystem.models import *

User = get_user_model()

def get_db_status(request : any) -> JsonResponse:
    db_connection = connections['default']
    try:
        db_connection.cursor()
    except OperationalError:
        connected = False
    else:
        connected = True
    return JsonResponse({'success': connected}, safe=False)

@api_view(['POST'])
def register(request):
    try:
        # Check if a user with the same email already exists
        if User.objects.filter(username=request.data['username']).exists():
            return JsonResponse({'success': False, 'msg': 'Email already registered'}, safe=False)
        # Create a new user
        user = User.objects.create_user(**request.data)
        user.save()
        return JsonResponse({'success': True, 'msg': 'Successfully registered'}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'msg': str(e)}, safe=False)
    
@api_view(['POST'])
def login(request):
    try:
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user is not None:
            # User is authenticated, login successful
            return JsonResponse({'success':True,'msg': "Successfully logged in", 'user':UserInfo.objects.all().filter(user=user).values()[0]}, safe=False)
        else:
            # User is not authenticated, login failed
            return JsonResponse({'success':False,'msg': "User doesn't exist"}, safe=False)
    except Exception as e:
            return JsonResponse({'success':False,'msg': str(e)}, safe=False)
    
@api_view(['POST'])
def delete_user(request:any) -> JsonResponse:
    try:
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None and user.is_superuser:
            deleted_user = User.objects.get(username=request.data['delete_username'])
            deleted_user.delete()
            return JsonResponse({'success':True,'msg': f'Successfully delete user {request.data["delete_username"]}'}, safe=False)
        else:
            return JsonResponse({'success':False,'msg': "You don't have a permission"}, safe=False)
    except Exception as e:
            return JsonResponse({'success':False,'msg': str(e)}, safe=False)
    
@api_view(['GET'])
def get_items(request: any) -> JsonResponse:
    stock_df = pd.DataFrame(data=StockItem.objects.values())
    stock_df['qty'] = 1
    stock_df = stock_df.replace({np.NaN: None})
    return JsonResponse(stock_df.to_dict('records'), safe=False)

@api_view(['GET'])
def get_customers(request: any) -> JsonResponse:
    customer_df = pd.DataFrame(data=UserInfo.objects.values())
    customer_df = customer_df.replace({np.NaN: None})
    return JsonResponse(customer_df.to_dict('records'), safe=False)

@api_view(['GET'])
def confirm_invoice(request: any) -> JsonResponse:
    try:
        params = {
            'id': request.GET.get('id'),
            'status': 'confirmed'
        }
        invoice = Invoice.objects.filter(id=params['id']).update(status=params['status'])
        return JsonResponse({'success': True}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)

@api_view(['GET'])
def create_user_by_json(request:any) -> JsonResponse:
    f = open(os.path.basename('customers_transformed.json'), 'r')
    customer_json = json.loads(f.read())
    for _,val in customer_json.items():
        try:
            request = {
                "username":"".join(val['name'].split()).lower(),
                "password":"12345",
                "is_superuser": 0,
                "last_login": datetime.datetime.now()
            }
            # Check if a user with the same email already exists
            if User.objects.filter(username=request['username']).exists():
                return JsonResponse({'success': False, 'msg': 'Username already registered'}, safe=False)
            # Create a new user
            user = User.objects.create_user(**request)
            user.save()
            val['created_at'] = val['date']
            val['instance_id'] = val['id']
            val['user'] = user
            del val['date']
            del val['id']
            UserInfo.objects.create(**val)
        except Exception as e:
            return JsonResponse({'success':False,'msg': str(e)}, safe=False)

    return JsonResponse({'success':True,'msg': "all user created"}, safe=False)

@api_view(['GET'])
def create_stock_by_json(request: any) -> JsonResponse:
    f = open(os.path.basename('Stock.json'), 'r')
    stock_json = json.loads(f.read())
    try:
        for _, val in stock_json.items():
            val_lower = {k.lower():v for k,v in val.items()}
            val_lower['id'] = val_lower['index']
            del val_lower['index']
            StockItem.objects.create(**val_lower)
        return JsonResponse({'success':True,'msg': "all items created"}, safe=False)
    except Exception as e:
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)

@api_view(['GET'])
def create_invoice(request: any) -> JsonResponse:
    try:
        params = {
            'id': Invoice.objects.count(),
            'customer': UserInfo.objects.get(instance_id = request.GET.get('customer')),
            'detail': request.GET.get('detail'),
            'status': request.GET.get('status'),
            'request_date': datetime.datetime.now(),
        }
        i = Invoice(**params)
        i.invoiceNumber = f'{datetime.datetime.today().year}-{i.id}'
        i.save()
        return JsonResponse({'success':True,'msg': "Created Invoices"}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)

def create_users():
    return JsonResponse({}, safe=False)

def set_users():
    return JsonResponse({}, safe=False)

def get_users():
    return JsonResponse({}, safe=False)

@api_view(['GET'])
def get_invioces(request: any) -> JsonResponse:
    try:
        invoices = Invoice.objects.filter(customer_id=UserInfo.objects.get(instance_id = request.GET.get('id'))).values()
        return JsonResponse(list(invoices), safe=False)
    except Exception as e:
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)
    
def get_items_in_invoice(request: any) -> JsonResponse:
    params = {
        'inv_id': request.GET.get('id')
    }
    items = InvoiceItems.objects.filter(**params).values()
    return JsonResponse(list(items), safe=False)

def add_items_to_invoice(request: any) -> JsonResponse:
    try:
        params = {
            'inv_id': request.GET.get('invoice_id'),
            'items': json.loads(request.GET.get('items'))
        }
        print(params)
        for item in params['items']:
            param = {
                'inv':Invoice.objects.get(id=params['inv_id']),
                'item_name':item['code'],
                'qty':item['qty'],
                'tax': 0.0,
                'price': item['unit_price']
            }
            print(param)
            InvoiceItems.objects.create(**param)
        return JsonResponse({'success':True}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)
    
def save_items_to_invoice(request: any) -> JsonResponse:
    try:
        params = {
            'items': json.loads(request.GET.get('items'))
        }
        print(params['items'])
        for item in params['items']:
            param = {
                'qty':item['qty'],
                'tax': float(item['tax']),
                'price': float(item['price'])
            }
            InvoiceItems.objects.filter(id=item['id']).update(**param)
        return JsonResponse({'success':True}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)
    
@api_view(['POST'])
def upload_stock_csv(request) -> JsonResponse:
    try:
        file = request.FILES['file'].read().decode('utf-8')
        import csv
        import io
        columns = ['id', 'detail', 'jm_id', 'be_id', 'unit_price', 'barcode_id', 'piece', 'discounted', 'qt', 'cost', 'code' , 'taxactive']
        df = pd.read_csv(io.StringIO(file), sep=',', columns=columns)
        # TODO: create or update an items
        return JsonResponse({'success':True}, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'msg': str(e)}, safe=False)

