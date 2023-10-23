from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from .permissions import IsAuthorOrSuperuser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

class Post(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = AuthorPost.objects.filter()

    permission_classes = [IsAuthorOrSuperuser, IsAuthenticated]
    http_method_names = ['post', 'get', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PostSerializer(data=data, many=False, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            context = {
                'create_post': PostSerializer(user, many=False, context={"request": request}).data,
            }
            return Response(context, status=status.HTTP_200_OK)
        elif serializer.errors:
            return Response({"detail": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        data = AuthorPost.objects.all().exclude(is_deleted=True)
        context = {
            'list_post' : PostSerializer(data, many=True, context={"request": request}).data
        }
        return Response(context, status=status.HTTP_200_OK)


    def destroy(self, request,pk):
        try:
            if AuthorPost.objects.filter(id=pk).exists():
                is_user_post = AuthorPost.objects.get(id=pk)
                self.check_object_permissions(request, is_user_post)
                is_user_post.is_deleted=True
                is_user_post.save()

                context = {
                    'detail': 'Post deleted successfully!!'
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Record not found."},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "you canot delete this post as this is not yours."},
                            status=status.HTTP_400_BAD_REQUEST)


    def update(self, request,pk):
        try:
            data = request.data

            if AuthorPost.objects.filter(id=pk).exists():
                post_obj = AuthorPost.objects.get(id=pk)
                self.check_object_permissions(request, post_obj)
                post_obj.title = data.get('title')
                post_obj.body = data.get('body')
                post_obj.auther = data.get('auther')
                post_obj.save()


                return Response({'list': PostSerializer(post_obj, many=False,
                                                         context={"request": request}).data
                                 }, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "you canot modify this post as this is not yours."},
                        status=status.HTTP_400_BAD_REQUEST)

class ListAllPost(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = AuthorPost.objects.filter()

    permission_classes = [IsAuthorOrSuperuser, IsAuthenticated]
    http_method_names = ['get',]

    def list(self, request,pk):
        if AuthorPost.objects.filter(id=pk).exists():
            data = AuthorPost.objects.get(id=pk)
            context = {
                'list_post': PostSerializer(data, many=False, context={"request": request}).data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Record not found."}, status=status.HTTP_400_BAD_REQUEST)


class Block(viewsets.ModelViewSet):
    serializer_class = BlockAuthorSerializer
    queryset = BlockAuthor.objects.filter()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        data = request.data
        if not data['block_to']==request.user:
            serializer = BlockAuthorSerializer(data=data, many=False, context={"request": request})
            if serializer.is_valid():
                user = serializer.save()
                context = {
                    'block': BlockAuthorSerializer(user, many=False, context={"request": request}).data,
                }
                return Response(context, status=status.HTTP_200_OK)
            elif serializer.errors:
                return Response({"detail": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Cannot block yourself"},
                            status=status.HTTP_400_BAD_REQUEST)

class ListBlockedUser(viewsets.ModelViewSet):
    serializer_class = BlockAuthorSerializer
    queryset = BlockAuthor.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get',]

    def list(self, request):
        data = BlockAuthor.objects.filter(block_by=request.user)
        context = {
            'list_blocked_user': BlockAuthorSerializer(data, many=True, context={"request": request}).data
        }
        return Response(context, status=status.HTTP_200_OK)


class UserUnBlock(viewsets.ModelViewSet):
    serializer_class = BlockAuthorSerializer
    queryset = BlockAuthor.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['delete']


    def delete(self,request,*args,**kwargs):
        pk = self.request.query_params.get('pk')

        if  BlockAuthor.objects.filter(id = pk).exists():
            user_obj = BlockAuthor.objects.filter(id = pk).delete()
            return Response({"detail": "deleted successfully."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Record not found."},
                            status=status.HTTP_400_BAD_REQUEST)

class FilterPost(viewsets.ModelViewSet):
    serializer_class = BlockAuthorSerializer
    queryset = BlockAuthor.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']


    def list(self,request,*args,**kwargs):
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')

        if title and author:
            data = AuthorPost.objects.filter(Q(title__icontains = title)|Q(author__name__icontains=author))
            data_count = data.count()
            page_number = request.query_params.get('page', 1)
            paginator = Paginator(data, 10)
            page_obj = paginator.get_page(page_number)

            context = {
                "prod_count": data_count,
                "result": True, "status": 200,
                "per_page": paginator.per_page,
                "num_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "next_page_number": page_obj.next_page_number() if page_obj.has_next() else 0,
                "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else 0,
                'list_post': PostSerializer(data, many=True, context={"request": request}).data

            }

            return Response(context, status=status.HTTP_200_OK)
        return Response({"detail": "please provide proper data."},
                        status=status.HTTP_400_BAD_REQUEST)


class AuthorListPostById(viewsets.ModelViewSet):
    serializer_class = BlockAuthorSerializer
    queryset = BlockAuthor.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']

    def list(self, request):
        id = self.request.query_params.get('author')
        data = AuthorPost.objects.filter(author=id).exclude(is_deleted = True)
        context = {
            'list_author_by_id': PostSerializer(data, many=True, context={"request": request}).data
        }
        return Response(context, status=status.HTTP_200_OK)