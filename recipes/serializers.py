from rest_framework import serializers
from tag.models import Tag
from .models import Recipe
from authors.validators import AuthorRecipeValidator
from django.core.exceptions import ValidationError


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class RecipesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit',
            'preparation_steps', 'cover']
    
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name="any_method_name", read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True, read_only=True)
    
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        read_only=True,
        view_name='recipes:recipes_api_v2_tag'
    )
    
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    def validate(self, attrs):
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=ValidationError)
        return super_validate