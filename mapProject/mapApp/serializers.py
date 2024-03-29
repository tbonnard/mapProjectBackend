from rest_framework import serializers
from .models import Property, Project, Choice, User, Follow, Vote


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'


    def get_properties(self, obj):
        selected_properties = Property.objects.filter(pk=obj.property.id).distinct()
        return PropertySerializer(selected_properties, many=True).data

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        # pour ne pas display le password en return
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Permet de hash le password lors du create user
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'email']


class FollowSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    class Meta:
        model = Follow
        # fields = '__all__'
        fields = ['id', 'follower', 'property', 'properties']


    def get_properties(self, obj):
        selected_properties = Property.objects.filter(pk=obj.property.id).distinct()
        return PropertySerializer(selected_properties, many=True).data


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
