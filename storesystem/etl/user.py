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
from storesystem.views import *
from datetime import datetime
def create_user_by_json():
    f = open(os.path.basename('customers_transformed.json'), 'r')
    customer_json = json.loads(f.read())
    customer_list = list()
    for _,val in customer_json.items():
        request = {
            "username":"".join(val['name']).lower(),
            "password":"12345",
            "is_superuser": 0,
            "last_login": datetime.now()
        }
        res = register(request=request)
        if(not res['success']):
            raise
        UserInfo.objects.create(**val)

    print('done')