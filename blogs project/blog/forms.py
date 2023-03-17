from django import forms 
from .models import Comment ,Blog,Category


class BlogForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name'))

    class Meta:
        model = Blog
        fields = ['title', 'featured_image', 'content','category']
        

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': 'form3Example1c'})


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ["content"]
        widgets = { 
            "content":forms.TextInput(attrs={"class":"form-control"},)
        }
