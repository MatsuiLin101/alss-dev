from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField,
    DateTimeField,
)
from logs.models import (
    ReviewLog,
)


class ReviewLogListSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    user = SerializerMethodField()
    content_object = SerializerMethodField()
    update_datetime = DateTimeField(format="%Y/%m/%d %H:%M:%S")

    def get_user(self, instance):
        return instance.user.username

    def get_content_object(self, instance):
        return instance.content_object.farmer_id

    class Meta:
        model = ReviewLog
        fields = '__all__'


class ReviewLogUpdateSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ReviewLog
        fields = '__all__'

    def create(self, validated_data):
        instance = ReviewLog.objects.create(
            user=validated_data['user'],
            content_type=validated_data['content_type'],
            object_id=validated_data['object_id'],
            initial_errors=0,
            current_errors=0,
        )
        if 'current_errors' in validated_data:
            instance.initial_errors = validated_data['current_errors']
            instance.current_errors = validated_data['current_errors']
            instance.save()
        return instance

    def update(self, instance, validated_data):
        if 'current_errors' in validated_data:
            instance.current_errors = validated_data['current_errors']
        instance.save()

        return instance
