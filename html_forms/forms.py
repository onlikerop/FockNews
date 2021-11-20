from Main.models import Articles, Views
from django.forms import ModelForm, TextInput, Textarea, Select


class CreateArticleForm(ModelForm):
    class Meta:
        model = Articles
        fields = ["title", "body", "tags", "status"]
        widgets = {
            "title": TextInput(
                attrs={
                    'type': "text",
                    'placeholder': "Название статьи",
                    'class': "form-control"
                }
            ),
            "body": Textarea(
                attrs={
                    'placeholder': "Текст статьи",
                    'class': "form-control"
                }
            ),
            "tags": TextInput(
                attrs={
                    'type': "text",
                    'placeholder': "Теги статьи",
                    'class': "form-control"
                }
            ),
            "status": Select(choices=(
                ("published", "Публикация"),
                ("draft", "Черновик"),
            ),
                attrs={
                    'class': "form-control"
                }
            )
        }