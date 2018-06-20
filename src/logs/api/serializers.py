from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField,
    DateTimeField,
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
    update_datetime = DateTimeField(format="%Y/%m/%d %H:%M:%S")

    def get_user(self, instance):
        if instance.user.first_name:
            return instance.user.first_name + instance.user.last_name
        else:
            return instance.user.username

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
