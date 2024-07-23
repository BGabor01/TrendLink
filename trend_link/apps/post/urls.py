from django.urls import path
from django.views.generic import TemplateView
from apps.post.views import (
    ListPostsView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
    CreateCommentView,
    DeleteCommentView,
    UpdateCommentView,
    LikePostView,
    UnlikePostView,
)

urlpatterns = [
    # API Endpoints
    path("api/create/", CreatePostView.as_view(), name="api_create_post"),
    path("api/list/", ListPostsView.as_view(), name="api_list_posts"),
    path("api/<int:pk>/update/", UpdatePostView.as_view(), name="api_update_post"),
    path("api/<int:pk>/delete/", DeletePostView.as_view(), name="api_delete_post"),
    path("api/comment/create/", CreateCommentView.as_view(),
         name="api_create_comment"),
    path("api/comment/<int:pk>/delete/",
         DeleteCommentView.as_view(), name="api_delete_comment"),
    path("api/comment/<int:pk>/update/",
         UpdateCommentView.as_view(), name="api_update_comment"),
    path("api/like/create/", LikePostView.as_view(), name="api_like_post"),
    path("api/like/<int:post_id>/remove/",
         UnlikePostView.as_view(), name="api_unlike_post"),

    # Template Views
    path("create/", TemplateView.as_view(template_name="post/post.html"),
         name="view_create_post"),
]
