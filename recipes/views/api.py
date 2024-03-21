from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Recipe
from ..serializers import RecipesSerializer
from ..serializers import TagSerializer
from tag.models import Tag
from django.shortcuts import get_object_or_404

@api_view(http_method_names = ['get', 'post'])
def recipe_api_list(request):
    if request.method == 'POST':
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED
            )
        return Response(
                        serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST
        )        
    
    
    recipes = Recipe.objects.get_published()               
    serializer = RecipesSerializer(instance=recipes, context={'request':request}, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.filter(pk=pk))
    serializer = RecipesSerializer(instance=recipe, many=False, context = {'request':request})
    return Response(serializer.data)

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
    