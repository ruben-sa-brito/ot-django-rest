from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Recipe
from ..serializers import RecipesSerializer
from django.shortcuts import get_object_or_404

@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()
    serializer = RecipesSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.filter(pk=pk))
    serializer = RecipesSerializer(instance=recipe, many=False)
    return Response(serializer.data)
    