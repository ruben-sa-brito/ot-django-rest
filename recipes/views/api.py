from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from ..models import Recipe
from ..serializers import RecipesSerializer
from ..serializers import TagSerializer
from tag.models import Tag
from django.shortcuts import get_object_or_404


class RecipeApiv2Pagination(PageNumberPagination):
    page_size = 100
class RecipeAPIv2List(ListCreateAPIView):
    
    queryset = Recipe.objects.get_published()
    serializer_class  = RecipesSerializer
    pagination_class = RecipeApiv2Pagination
    
class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    
    queryset = Recipe.objects.get_published()
    serializer_class  = RecipesSerializer
    pagination_class = RecipeApiv2Pagination   
        
@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(serializer.data)
    