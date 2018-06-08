import csv
from rest_framework import serializers
from surveys18.models import BuilderFile
from surveys18.builder.tokenizer import Builder


class BuilderFieldSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuilderFile
        fields = ['datafile']

    def create(self, validated_data):
        return BuilderFile.objects.create(**validated_data)

    def validate(self, data):
        """
        Validate via build
        """
        data_list = str(data.get('datafile').read()).splitlines()

        for string in data_list:
            builder = Builder(string)
            builder.build_survey()

        return data