from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Index page')

def user_reg(request):
    return HttpResponse('Reg page')
    
def user_auth(request):
    return HttpResponse('Auth page')
