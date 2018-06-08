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
        errors = list()
        data_list = str(data.get('datafile').read()).splitlines()

        for i, string in enumerate(data_list):
            try:
                builder = Builder(string)
                builder.build_survey()
            except Exception as e:
                errors.append({
                    'string': string,
                    'index': i,
                    'error': e,
                })
                pass

        if errors:
            raise serializers.ValidationError(errors)

        return data