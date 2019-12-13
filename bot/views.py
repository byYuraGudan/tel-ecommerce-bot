from django.http import HttpResponse
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def liqpay(request):
    logger.info(request, request.data)
    return HttpResponse('')
