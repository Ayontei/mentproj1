from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

def index(request):
    return HttpResponse('Index page')

def get_post(request, post_id):
    return HttpResponse(f'You revice post with id {post_id}')

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Not found<h1>')