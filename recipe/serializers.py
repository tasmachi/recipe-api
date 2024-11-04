from core.models import Recipe,Tag,Ingredient
from rest_framework import serializers


class TagSerealizer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields=['id','name']
        read_only_field=['id']

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model=Ingredient
        fields=['id','name']
        read_only_fields=['id']

class RecipeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Recipe
        fields=['id','image']
        read_only_fields=['id']
        extra_kwargs={'image':{'required':'True'}}

class RecipeSerializer(serializers.ModelSerializer):
    tags=TagSerealizer(many=True,required=False)
    ingredients=IngredientSerializer(many=True,required=False)

    class Meta:
        model=Recipe
        fields=['id','title','time_minutes','price','link','tags','ingredients']
        read_only_fields=['id']

    def _get_or_create_tags(self,tags,recipe):
        auth_user=self.context['request'].user

        #Create or get tags
        for tag_data in tags:
            tag, created=Tag.objects.get_or_create(user=auth_user,**tag_data)
            recipe.tags.add(tag)

    def _get_or_create_ingredient(self,ingredients,recipe):
        auth_user=self.context['request'].user

        for ingredient in ingredients:
            ing_obj,created=Ingredient.objects.get_or_create(user=auth_user, **ingredient)
            recipe.ingredients.add(ing_obj)

    def create(self,validated_data):
        tags_data=validated_data.pop('tags',[])
        ing_data=validated_data.pop('ingredients',[])
        recipe=Recipe.objects.create(**validated_data)

        self._get_or_create_tags(tags_data,recipe)
        self._get_or_create_ingredient(ing_data,recipe)

        return recipe

    def update(self,instance,validated_data):
        tags_data=validated_data.pop('tags',None)
        ing_data=validated_data.pop('ingredients',None)

        if tags_data is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags_data,instance)

        if ing_data is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredient(ing_data,instance)

        for attr, value in validated_data.items():
            setattr(instance,attr,value)

        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):

    class Meta(RecipeSerializer.Meta):
        fields=RecipeSerializer.Meta.fields + ['description','image']
