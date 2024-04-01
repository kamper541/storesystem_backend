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

def read_stock():
    f = open('Stock.json')
    data = json.load(f)
    model_list = []
    d_keys = data.keys()
    for i in d_keys:
        inst = {k.lower(): v for k,v in data[i].items()}
        inst.pop('index')