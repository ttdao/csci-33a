from django import forms
from .models import Comment, Post, Tag


# tags = Tag.objects.all().values_list('name', 'name')
#
# tag_list = []
#
# for choice in tags:
#     tag_list.append(choice)


class CreatePost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Title',
                                                          'aria-label': 'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Start Typing!',
                                                           'aria-label': 'Start Typing!'}))
    tag = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         queryset=Tag.objects.all(),
                                         )

    class Meta:
        model = Post


class EditPost(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tag = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         queryset=Tag.objects.all(),
                                         )

    class Meta:
        model = Post


class CreateComment(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Leave a comment',
                                                           'aria-label': 'Leave a comment'}), )

    class Meta:
        model = Comment
