from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def subscribe(request):
    if not request.user.is_authenticated:
        return Response({'Err':'Вам нужно авторизоваться'})
    
    return Response({'message':'Вы подписались на :'})


@api_view(['GET','DELETE'])
def get_status(request):
    if not request.user.is_authenticated:
        return Response({'Err':'Вам нужно авторизоваться'})
    
    target_user_id = request.data.get('user_id')
    
    if request.method == 'GET':
        return Response({'message':f'Вы подписаны на :{target_user_id}'})
    elif request.method == 'DELETE':
        return Response({'message':f'Вы отписались от :{target_user_id}'})