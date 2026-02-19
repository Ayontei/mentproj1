from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Index page')

def get_post(request, post_id):
    return HttpResponse(f'You revice post with id {post_id}')