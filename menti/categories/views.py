from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from .models import Category

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.values_list('name', flat=True)
        # serializer = CategorySerializer(category, many=True)
        return Response(list(category))
    
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({'error': 'Только для администраторов'}, status=403)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # создает категорию в БД
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET','PUT','PATCH', 'DELETE'])
def get_category(request, category_id):
    # Все методы кроме GET требуют админа
    if request.method != 'GET' and not request.user.is_staff:
        return Response({'error': 'Только для администраторов'}, status=403)
    
    try:
        category = Category.objects.get(id=category_id)  # получаем тег один раз для всех методов
    except Category.DoesNotExist:
        return Response({'Err': 'Категория не найден'}, status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': f'Категория {category_id} удалена'}, status=204)
