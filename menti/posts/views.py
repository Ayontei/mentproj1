from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Post  # ваша модель



@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    return HttpResponse('Index page')


@api_view(['GET'])
@permission_classes([AllowAny])
def get_post(request, post_id):
    return HttpResponse(f'You revice post with id {post_id}')

@api_view(['GET'])
@permission_classes([AllowAny])
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Not found<h1>')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request, post_id):
    return HttpResponse(f'You revice post with id {post_id}')


