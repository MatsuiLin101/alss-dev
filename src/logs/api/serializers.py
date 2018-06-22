from django.utils import timezone
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField,
    RelatedField,
)
from logs.models import (
    ReviewLog,
)
from surveys18.models import Survey as Survey18


class ContentObjectRelatedField(RelatedField):
    """
    A custom field to use for the `content_object` generic relationship.
    """
    def to_representation(self, value):
        """
        Serialize content objects to a simple textual representation.
        """
        if isinstance(value, Survey18):
            return value.farmer_id
        raise Exception('Unexpected type of content object')


class ReviewLogListSerializer(ModelSerializer):
    id = IntegerField(read_only=False)
    user = SerializerMethodField()
    content_object = ContentObjectRelatedField(read_only=True)
    update_datetime = SerializerMethodField()

    def get_user(self, instance):
        if instance.user.first_name:
            return instance.user.first_name + instance.user.last_name
        else:
            return instance.user.username

    def get_update_datetime(self, instance):
        return timezone.localtime(instance.update_datetime).strftime('%Y/%m/%d %H:%M:%S')

    class Meta:
        model = ReviewLog
        fields = '__all__'


class ReviewLogUpdateSerializer(ModelSerializer):
    id = IntegerField(read_only=False)

    class Meta:
        model = ReviewLog
        fields = '__all__'

    def create(self, validated_data):
        content_type = validated_data['content_type']
        object_id = validated_data['object_id']

        if content_type and object_id:
            obj = ReviewLog.objects.filter(content_type=content_type,
                                           object_id=object_id).order_by('update_datetime').first()
            if obj:
                initial_errors = obj.initial_errors if obj else None
            else:
                initial_errors = validated_data['current_errors'] if 'current_errors' in validated_data else None

            current_errors = validated_data['current_errors'] if 'current_errors' in validated_data else None

            instance = ReviewLog.objects.create(
                user=validated_data['user'],
                content_type=content_type,
                object_id=object_id,
                initial_errors=initial_errors,
                current_errors=current_errors,
            )
            return instance

    def update(self, instance, validated_data):
        if 'current_errors' in validated_data:
            instance.current_errors = validated_data['current_errors']
            instance.save()

        return instance
