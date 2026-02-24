from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TagSerializer
from .models import Tags

@api_view(['GET', 'POST'])
def tags_list(request):
    if request.method == 'GET':
        tags = Tags.objects.values_list('name', flat=True)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error': 'Только для администраторов'}, status=403)
        
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # создает тег в БД
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET','PUT','PATCH', 'DELETE'])
def get_tag(request, tag_id):
    # Все методы кроме GET требуют админа
    if request.method != 'GET' and not request.user.is_staff:
        return Response({'error': 'Только для администраторов'}, status=403)
    
    try:
        tag = Tags.objects.get(id=tag_id)  # получаем тег один раз для всех методов
    except Tags.DoesNotExist:
        return Response({'Err': 'Тэг не найден'}, status=404)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        tag.delete()
        return Response({'message': f'Тэг {tag_id} удален'}, status=204)
