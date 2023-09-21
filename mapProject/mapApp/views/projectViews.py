import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import Http404

from ..serializers import ProjectSerializer, PropertySerializer
from ..models import Project, Property, User, Follow

from .propertyViews import PropertyCheckView

#projects related to a property
class ProjectsView(APIView):
    def post(self, request):
        if (Property.objects.filter(osm_id=request.data['osm_id'], osm_type=request.data['osm_type'])):
            queryset = Project.objects.filter(property=Property.objects.filter(osm_id=request.data['osm_id'], osm_type=request.data['osm_type']).first()).order_by('-created')
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data)
        queryset = Project.objects.none()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)


class ProjectsUserFollowedPropertyView(APIView):
    def post(self, request):
        propertiesFollowedbyUser = [i.property for i in Follow.objects.filter(follower=User.objects.get(pk=request.data['user']))]
        projectsToReturn = Project.objects.filter(property__in=propertiesFollowedbyUser).order_by('-created')
        serializer = ProjectSerializer(projectsToReturn, many=True)
        return Response(serializer.data)


class ProjectView(APIView):
    def get(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if (Property.objects.filter(osm_id=request.data['property']['osm_id'], osm_type=request.data['property']['osm_type'])):
            property=Property.objects.filter(osm_id=request.data['property']['osm_id'], osm_type=request.data['property']['osm_type']).first()
            creator = User.objects.get(pk=request.data['user']['id'])
            newProject = Project(property=property, title=request.data['title'], description=request.data['description'], creator=creator)
            newProject.save()
            if property.with_suggestions is False:
                property.with_suggestions = True
                property.save()
            serializer = ProjectSerializer(newProject)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializerProperty = PropertySerializer(data=request.data['property'])
            if serializerProperty.is_valid(raise_exception=True):
                serializerProperty.save()
                property = Property.objects.get(pk=serializerProperty.data['id'])
                creator = User.objects.get(pk=request.data['user']['id'])
                newProject = Project(property=property, title=request.data['title'],
                                     description=request.data['description'], creator=creator)
                newProject.save()
                if property.with_suggestions is False:
                    property.with_suggestions = True
                    property.save()
                serializer = ProjectSerializer(newProject)
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectAllNearbyView(APIView):
    def post(self, request):
        allProperties = request.data
        allProjects = []
        for i in allProperties:
            try:
                projectsFromProperty = Project.objects.filter(property=Property.objects.get(pk=i['id']))
                for y in projectsFromProperty:
                    allProjects.append(y)
            except:
                pass
        serializer = ProjectSerializer(allProjects, many=True)
        return Response(serializer.data)

class ProjectDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ProjectSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = ProjectSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)