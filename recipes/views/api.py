from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Recipe
from ..serializers import RecipesSerializer
from ..serializers import TagSerializer
from tag.models import Tag
from django.shortcuts import get_object_or_404

class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()               
        serializer = RecipesSerializer(instance=recipes, context={'request':request}, many=True)
        return Response(serializer.data)
    
    def post(self, request):
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
class RecipeAPIv2Detail(APIView):
    
    def get_recipe(self, pk):
        return get_object_or_404(Recipe.objects.filter(pk=pk))
    
    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipesSerializer(instance=recipe, many=False, 
                                       context = {'request':request})
        return Response(serializer.data)
    
    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipesSerializer(instance=recipe,
                                       data=request.data,
                                       many=False, 
                                       context={'request':request},
                                       partial=True,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                        serializer.data
        )
    
    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()
        return Response(status=status.HTTP_200_OK)    
        
@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
    