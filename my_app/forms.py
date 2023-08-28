from django import forms
from . import models


class GroupForm(forms.ModelForm):
    class Meta():
        model = models.Group
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Заголовок'
        self.fields['description'].label = 'Описание'


class PostForm(forms.ModelForm):
    class Meta():
        model = models.Post
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control post-create'})
        }
        labels = {
            'text': "Создайте пост"
        }
