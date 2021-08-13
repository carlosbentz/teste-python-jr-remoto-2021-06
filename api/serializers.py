from rest_framework import serializers
import requests
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ipdb import set_trace

from .models import PackageRelease, Project


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ['name', 'version']
        extra_kwargs = {'version': {'required': False}}


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'packages']

    packages = PackageSerializer(many=True)

    # def create(self, validated_data):
    #     # TODO
    #     # - Processar os pacotes recebidos
    #     # - Persistir informações no banco
    #     packages = validated_data.pop("packages")

    #     for package in packages:
    #         set_trace()
    #         package_name = package.get("name")
    #         package_version = package.get("version")
    #         r = requests.get(f'https://pypi.org/pypi/{package_name}/json')

    #         if r.status_code != 200:
    #             return Response(
    #                 {"error": "One or more packages don't exist"},
    #                 status=status.HTTP_400_BAD_REQUEST
    #                 )

    #         releases = r.json()["releases"]

    #         if not package_version:
    #             package_datas = []
    #             for key, value in releases.items():
    #                 if value:
    #                     date = datetime.strptime(
    #                         value[0]["upload_time"], "%Y-%m-%dT%H:%M:%S"
    #                     )
    #                     package_datas.append(date)

    #                     if date == max(package_datas):
    #                         package_version = key

    #             if not package_datas:
    #                 package_version = "1.0"

    #         else:
    #             if not releases.get(package_version):
    #                 return Response(
    #                     {"error": "One or more packages don't exist"},
    #                     status=status.HTTP_400_BAD_REQUEST
    #                     )

    #         package["version"] = package_version

    #     project = Project.objects.create(**validated_data)

    #     for package in packages:

    #         package = PackageRelease.objects.create(
    #             **package,
    #             project_id=project.id
    #         )

    #         project.packages.add(package)

    #     return project
