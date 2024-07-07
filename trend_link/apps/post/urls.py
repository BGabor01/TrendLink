from django.urls import path
from apps.post.views import PostView, ListPostView, CreatePostView

urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("list/", ListPostView.as_view(), name="list-post"),
    path("<int:pk>/", PostView.as_view(), name="post"),
]
