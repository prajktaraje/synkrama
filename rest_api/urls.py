from django.urls import re_path as url,include
from rest_framework import routers
from accounts import views as accounts_views
router = routers.DefaultRouter()

router.register(r'posts', accounts_views.Post, basename='post')
router.register(r'posts/<int:id>/', accounts_views.ListAllPost, basename='list_by_id')
router.register(r'block-user', accounts_views.Block, basename='block-user')
router.register(r'get-blocked-user', accounts_views.ListBlockedUser, basename='get-blocked-user')
router.register(r'user_unblock', accounts_views.UserUnBlock, basename="user_unblock"),
router.register(r'filter_post', accounts_views.FilterPost, basename="filter_post"),
router.register(r'author_post_by_id', accounts_views.AuthorListPostById, basename="author_post_by_id"),


urlpatterns = [
    url(r'', include(router.urls)),
    ]