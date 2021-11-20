from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    last_login = serializers.DateTimeField()


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    avatar = serializers.CharField()
    rank = serializers.CharField(max_length=64)
    about_me = serializers.CharField()
    birthday_date = serializers.DateField()


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=120)
    body = serializers.CharField()
    create_datetime = serializers.DateTimeField()
    pub_datetime = serializers.DateTimeField()
    lasted_datetime = serializers.DateTimeField()
    author_id = serializers.IntegerField()
    tags = serializers.CharField()
    status = serializers.CharField(max_length=24)


