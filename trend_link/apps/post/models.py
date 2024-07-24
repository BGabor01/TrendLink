from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

from apps.post.managers import PostManager


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts", related_query_name="posts"
    )
    text = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="post_images/")
    tags = ArrayField(models.CharField(max_length=50),
                      null=True, blank=True, size=8)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self) -> str:
        return f"Post by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def get_number_of_likes(self):
        return self.likes.count()

    def get_number_of_comments(self):
        return self.comments.count()

    objects = PostManager()

    class Meta:
        app_label = "post"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comments",
    )
    text = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Comment on Post {self.post.pk}"

    class Meta:
        app_label = "post"
        indexes = [
            models.Index(fields=["user", "post"]),
        ]


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes", related_query_name="likes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", related_query_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Like on Post: {self.post.pk} by {self.user.username}"

    class Meta:
        app_label = "post"
        unique_together = ("user", "post")
        indexes = [
            models.Index(fields=["user", "post"]),
        ]
