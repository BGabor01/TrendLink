from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.post.forms import PostForm, ListPostForm


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "post/post.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect("home").url


class ListPostView(LoginRequiredMixin, ListView):
    from apps.post.models import Post

    form_class = ListPostForm
    queryset = Post.objects.all()
    ordering = ["-created_at"]
    paginate_by = 10
    context_object_name = "posts"

    def get_success_url(self):
        return redirect("home").url

    def get_permission_denied_message(self) -> str:
        return "You have to be logged in to check a profile!"

    def get_login_url(self) -> str:
        return "login"


class PostView(LoginRequiredMixin, UpdateView):
    from apps.post.models import Post

    model = Post
    form_class = PostForm
    template_name = "post/post.html"
    queryset = Post.objects.all()

    def get_success_url(self):
        return redirect("home").url

    def get_permission_denied_message(self) -> str:
        return "You have to be logged in to check a profile!"

    def get_login_url(self) -> str:
        return "login"
