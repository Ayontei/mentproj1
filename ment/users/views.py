from django.shortcuts import render
from django.http import HttpResponse


def user_reg(request):
    return HttpResponse('Reg page')
    
def user_auth(request):
    return HttpResponse('Auth page')
