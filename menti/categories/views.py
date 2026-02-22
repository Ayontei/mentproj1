from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        return Response({'message':'all category list'})
    elif request.method == 'POST':
        if not request.user.is_staff:  # или is_superuser
            return Response({'error': 'Только для администраторов'}, status=403)
        return Response({'message':'your category created'})

@api_view(['GET','PUT','PATCH', 'DELETE'])
def get_category(request, id):
    # Все методы кроме GET требуют админа
    if request.method != 'GET' and not request.user.is_staff:
        return Response({'error': 'Только для администраторов'}, status=403)
    
    if request.method == 'GET':
        return Response({'message':f'detail category {id}'})
    elif request.method == 'PUT':
        return Response({'message':f'this category update all {id}'})
    elif request.method == 'PATCH':
        return Response({'message':f'this category updated {id}'})
    elif request.method == 'DELETE':
        return Response({'message':f'this category deleted {id}'})
