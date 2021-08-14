from rest_framework import serializers
import requests
from datetime import datetime

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

    def create(self, validated_data):
        packages = validated_data.pop("packages")

        for package in packages:
            package_name = package.get("name")
            package_version = package.get("version")
            r = requests.get(f'https://pypi.org/pypi/{package_name}/json')

            if r.status_code != 200:
                raise serializers.ValidationError(
                    {"error": "One or more packages doesn't exist"}
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
                    raise serializers.ValidationError(
                        {"error": "One or more packages doesn't exist"}
                    )

            package["version"] = package_version

        project = Project.objects.create(**validated_data)

        for package in packages:

            package = PackageRelease.objects.create(
                **package,
                project_id=project.id
            )

            project.packages.add(package)

        return project
