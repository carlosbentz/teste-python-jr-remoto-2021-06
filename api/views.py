from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests
from ipdb import set_trace
from datetime import datetime

from .serializers import ProjectSerializer
from .models import PackageRelease, Project


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    # lookup_field = "name"
    serializer_class = ProjectSerializer

    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.queryset, name__iexact=pk)
        serializer_class = ProjectSerializer(project)

        return Response(serializer_class.data)

    def create(self, validated_data):
        # TODO
        # - Processar os pacotes recebidos
        # - Persistir informações no banco
        set_trace()
        packages = validated_data.data.pop("packages")
        for package in packages:
            package_name = package.get("name")
            package_version = package.get("version")
            r = requests.get(f'https://pypi.org/pypi/{package_name}/json')

            if r.status_code != 200:
                return Response(
                    {"error": "One or more packages don't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                    )

            releases = r.json()["releases"]

            if not package_version:
                package_datas = []
                for key, value in releases.items():
                    if value:
                        date = datetime.strptime(
                            value[0]["upload_time"], "%Y-%m-%dT%H:%M:%S"
                        )
                        package_datas.append(date)

                        if date == max(package_datas):
                            package_version = key

                if not package_datas:
                    package_version = "1.0"

            else:
                if not releases.get(package_version):
                    return Response(
                        {"error": "One or more packages don't exist"},
                        status=status.HTTP_400_BAD_REQUEST
                        )

            package["version"] = package_version

        project = Project.objects.create(**validated_data.data)

        for package in packages:

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )

            project.packages.add(package)

        project = ProjectSerializer(project)
        return Response(project.data, status=status.HTTP_201_CREATED)
