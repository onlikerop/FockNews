from datetime import datetime

from rest_framework import serializers

from API.models import APIKey
from Main.models import Articles
from Users.models import Bans


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
    avatar = serializers.CharField(
        required=False,
        allow_null=True
    )
    rank = serializers.CharField(
        max_length=64,
        required=False,
        allow_null=True
    )
    about_me = serializers.CharField(
        required=False,
        allow_null=True
    )
    birthday_date = serializers.DateField(
        required=False,
        allow_null=True
    )


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=120)
    body = serializers.CharField(
        required=False,
        allow_null=True
    )
    create_datetime = serializers.DateTimeField(default=datetime.now())
    pub_datetime = serializers.DateTimeField(
        required=False,
        allow_null=True,
        default=datetime.now()
    )
    lasted_datetime = serializers.DateTimeField(
        required=False,
        allow_null=True
    )
    author_id = serializers.IntegerField()
    tags = serializers.CharField(
        required=False,
        allow_null=True
    )
    status = serializers.CharField(
        max_length=24,
        default="published"
    )

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)


class APIKeySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    key = serializers.CharField()
    issue_datetime = serializers.DateTimeField(
        required=False,
        default=datetime.now()
    )
    exp_datetime = serializers.DateTimeField()
    issued_by_id = serializers.IntegerField()
    purpose = serializers.CharField()
    allowed_requests = serializers.IntegerField(default=100)
    status = serializers.CharField(default='Active')
    super_key = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return APIKey.objects.create(**validated_data)


class APIRequestSerializer(serializers.Serializer):
    APIKey_id = serializers.IntegerField
    ip = serializers.CharField(
        max_length=16,
        required=False,
        allow_null=True
    )
    datetime = serializers.DateTimeField(default=datetime.now())
    body = serializers.CharField()
    free = serializers.BooleanField(default=False)


class BansSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    reason = serializers.CharField(
        required=False,
        allow_null=True
    )
    who_banned_id = serializers.IntegerField()
    ban_datetime = serializers.DateTimeField(default=datetime.now())
    pass_datetime = serializers.DateTimeField()
    status = serializers.CharField(
        max_length=24,
        default='Active'
    )
    admin_note = serializers.CharField(
        required=False,
        allow_null=True
    )

    def create(self, validated_data):
        return Bans.objects.create(**validated_data)
