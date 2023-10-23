from rest_framework import serializers
from rest_framework.viewsets import ViewSet

from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email')

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    class Meta:
        model = AuthorPost
        fields = ('id','title','body','author')

    def create(self, validated_data):
        request = self.context.get('request')
        post_obj = AuthorPost.objects.create(**validated_data)
        post_obj.title = request.data['title']
        post_obj.body = request.data['body']
        user_obj = User.objects.get(id=request.data['author'])
        post_obj.author = user_obj
        post_obj.save()
        return post_obj


class BlockAuthorSerializer(serializers.ModelSerializer):
    blocked_to = UserSerializer(read_only=True, many=False)
    block_by = UserSerializer(read_only=True, many=False)

    class Meta:
        model = BlockAuthor
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        block_obj,flag = BlockAuthor.objects.get_or_create(**validated_data)
        block_to = User.objects.get(id=request.data['block_to'])
        block_obj.blocked_to = block_to
        block_obj.block_by = User.objects.get(id=request.user.id)
        block_obj.save()
        return block_obj