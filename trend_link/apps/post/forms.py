from django import forms


class PostForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        image = cleaned_data.get("image")

        if not text and not image:
            raise forms.ValidationError(
                "At least one of Text or Image must be provided."
            )

        return cleaned_data

    class Meta:
        from apps.post.models import Post

        model = Post
        fields = ["text", "image"]
        widgets = {
            "text": forms.Textarea(attrs={"required": False}),
            "image": forms.ClearableFileInput(attrs={"required": False}),
        }


class ListPostForm(forms.ModelForm):

    class Meta:
        from apps.post.models import Post

        model = Post
        fields = "__all__"
