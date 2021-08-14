from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProjectSerializer
from .models import Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.queryset, name__iexact=pk)
        serializer_class = ProjectSerializer(project)

        return Response(serializer_class.data)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, name__iexact=pk)   
        project.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
