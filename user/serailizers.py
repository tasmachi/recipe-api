from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model"""

    class Meta:
        model=get_user_model()
        fields=['email','name','password']
        extra_kwargs={'password':{'write_only':True},'min_length':5}

    def create(self, validated_data):
        print("Validated Data:", validated_data)  # Debugging line
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        password=validated_data.pop('password',None)
        user=super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the auth token."""
    email=serializers.EmailField()
    password=serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self,attrs):
        """Validate and authenticate the user"""
        email=attrs.get('email')
        password=attrs.get('password')
        user=authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg=['Unable to authenticate with provided credentials']
            raise serializers.ValidationError(msg,code='authorizatoin')
        attrs['user']=user
        return attrs