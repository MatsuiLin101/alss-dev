from rest_framework import serializers
from surveys18 import models


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Survey
        fields = ('__all__')


class ShortTermHireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ShortTermHire
        fields = ('__all__')


class LongTermHireSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LongTermHire
        fields = ('__all__')


class NumberWorkersSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NumberWorkers
        fields = ('__all__')


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkType
        fields = ('__all__')


class AgeScopeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AgeScope
        fields = ('__all__')
