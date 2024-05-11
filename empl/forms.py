from django import forms
from django.core.exceptions import ValidationError

from empl.models import Manuals, Category


class AddPostManual(forms.ModelForm):
    class Meta:
        model = Manuals
        fields = ['title', 'content', 'photo', 'cat',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title
