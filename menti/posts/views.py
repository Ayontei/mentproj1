from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post  # ваша модель



@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        return Response({'message':'all post list'})
    elif request.method == 'POST':
        if not request.user.is_authenticated:  # или is_superuser
            return Response({'error': 'Только для авторизованных пользователей'}, status=403)
        return Response({'message':'your post created'})
    
@api_view(['GET','PUT','PATCH', 'DELETE'])
def get_post(request, id):
    # Все методы кроме GET требуют админа
    if request.method != 'GET' and not request.user.is_staff:
        return Response({'error': 'Только для администраторов'}, status=403)
    
    if request.method == 'GET':
        return Response({'message':f'detail post {id}'})
    elif request.method == 'PUT':
        return Response({'message':f'this post update all {id}'})
    elif request.method == 'PATCH':
        return Response({'message':f'this post updated {id}'})
    elif request.method == 'DELETE':
        return Response({'message':f'this post deleted {id}'})
    
def page_not_found(request, exception):
    return Response({'Err':'Страница не найдена'})

