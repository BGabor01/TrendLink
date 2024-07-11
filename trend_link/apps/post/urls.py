from django.urls import path
from django.views.generic import TemplateView
from apps.post.views import (
    ListPostsView,
    CreatePostView,
    CreateCommentView,
    DeleteCommentView,
    UpdateCommentView,
    CreateLikeView,
    UpdatePostView,
)

urlpatterns = [
    path("api/create/", CreatePostView.as_view(), name="create-post-api"),
    path(
        "create/",
        TemplateView.as_view(template_name="post/post.html"),
        name="create-post",
    ),
    path("api/list/", ListPostsView.as_view(), name="list-post-api"),
    path("api/comment/create/", CreateCommentView.as_view(), name="create-comment-api"),
    path("api/<int:pk>/update/", UpdatePostView.as_view(), name="update-post-api"),
    path("api/<int:pk>/delete/", UpdatePostView.as_view(), name="delete-post-api"),
    path(
        "api/comment/<int:pk>/delete/",
        DeleteCommentView.as_view(),
        name="delete-comment-api",
    ),
    path(
        "api/comment/<int:pk>/update/",
        UpdateCommentView.as_view(),
        name="update-comment-api",
    ),
    path("api/like/create/", CreateLikeView.as_view(), name="create-like-api"),
]
