from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()



class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self,data):

        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username already exists in the database.')
            
            if data['email']:
                if User.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError('Email already exists in the database.')
        return data
    
    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    




class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model=Color
        fields=['color_name']

class PeopleSerializer(serializers.ModelSerializer):
    #color=ColorSerializer()
   # color_code=serializers.SerializerMethodField()
    class Meta:
        model=Person
        fields='__all__'
        #depth=1

    #def get_color_code(self,count):
     #   color_count=Color.objects.get(id=count.color.id)
      #  return {'color_name':color_count.color_name, 'hex_code':'#0000'}

    def validate(self, data):
        specialcharacters="!@#$%^&*()_+*/,./-"
        if any(c in specialcharacters for c in data['name']):
            raise serializers.ValidationError("The Name Should not contain Any Special Character")

        if data['age'] < 18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data
    
