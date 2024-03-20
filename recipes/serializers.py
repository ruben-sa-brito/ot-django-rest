from rest_framework import serializers
from tag.models import Tag
from .models import Recipe
from attr import attr


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class RecipesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ['id','title','description','author','category','tags','public','preparation','servings','preparation_time','tag_links']
    
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

        title = attrs['title']
        description = attrs['description']

        if title == description:
            raise serializers.ValidationError(
                {
                    "title": ["titulo nao pode ser igual a descriçao"],
                    "description": ["descriçao nao pode ser igual ao titulo"],
                }
            )

        return super_validate
    
    
    def validate_title(self, value):
        
        if len(value) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        
        return value
            