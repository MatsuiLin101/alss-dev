from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    ChoiceField,
)
from surveys18.models import (
    BuilderFile,
    BuilderFileType,
)
from surveys18.builder.tokenizer import Builder


class BuilderFileTypeSerializer(ModelSerializer):
    class Meta:
        model = BuilderFileType
        fields = '__all__'


class BuilderFileSerializer(HyperlinkedModelSerializer):
    type = ChoiceField(choices=BuilderFileType.objects.all())

    class Meta:
        model = BuilderFile
        fields = ['datafile', 'type']

    def create(self, validated_data):
        return BuilderFile.objects.create(**validated_data)

    def validate(self, data):
        """
        Validate via build
        """
        errors = list()
        data_list = str(data.get('datafile').read().decode('utf-8-sig')).splitlines()

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