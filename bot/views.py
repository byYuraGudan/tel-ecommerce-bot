from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def liqpay(request):
    print(request, request.data)
    return HttpResponse()