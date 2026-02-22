from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def tags_list(request):
    if request.method == 'GET':
        return Response({'message':'all tags list'})
    elif request.method == 'POST':
        if not request.user.is_staff:  # или is_superuser
            return Response({'error': 'Только для администраторов'}, status=403)
        return Response({'message':'your tag created'})
    
@api_view(['GET','PUT','PATCH', 'DELETE'])
def get_tag(request):
    # Все методы кроме GET требуют админа
    if request.method != 'GET' and not request.user.is_staff:
        return Response({'error': 'Только для администраторов'}, status=403)
    
    if request.method == 'GET':
        return Response({'message':'detail tag'})
    elif request.method == 'PUT':
        return Response({'message':'this tag update all'})
    elif request.method == 'PATCH':
        return Response({'message':'this tag updated'})
    elif request.method == 'DELETE':
        return Response({'message':'this tag deleted'})