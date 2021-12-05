from rest_framework import serializers

from Main.models import Articles


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    last_login = serializers.DateTimeField()


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    avatar = serializers.CharField(required=False)
    rank = serializers.CharField(max_length=64, required=False)
    about_me = serializers.CharField(required=False)
    birthday_date = serializers.DateField(required=False)


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=120)
    body = serializers.CharField(required=False)
    create_datetime = serializers.DateTimeField()
    pub_datetime = serializers.DateTimeField(required=False)
    lasted_datetime = serializers.DateTimeField(required=False)
    author_id = serializers.IntegerField()
    tags = serializers.CharField(required=False)
    status = serializers.CharField(max_length=24)

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)


class APIKeySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    key = serializers.CharField()
    issue_datetime = serializers.DateTimeField(required=False)
    exp_datetime = serializers.DateTimeField()
    issued_by_id = serializers.IntegerField()
    purpose = serializers.CharField()
    allowed_requests = serializers.IntegerField()
    status = serializers.CharField()
    super_key = serializers.BooleanField()
