from django import forms
from .models import Comment, Post, Tag

tags = [
    ('LEARNING', "Learning"),
    ('JAVASCRIPT', "Javascript"),
    ('WEBDEV', "Web Dev"),
    ('PYTHON', "Python"),
    ('GAME DESIGN', "Game Design"),
    ('BOOK', 'Books'),
    ('JUSTME', 'Just me'),
]


# tags = Tag.objects.all().values_list('name', 'name')
#
# tag_list = []
#
# for choice in tags:
#     tag_list.append(choice)


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ('title', 'content', 'tag')
        fields = ('title', 'content')
        tag = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Tag.objects.all(),
                                             )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title',
                                            'aria-label': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Start Typing!',
                                             'aria-label': 'Start Typing!'}),
            # 'tag': forms.Select(choices=tags, attrs={'class': 'form-control'}),

        }


class EditPost(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ('title', 'content', 'tag')
        fields = ('title', 'content')
        tag = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Tag.objects.all(),
                                             )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            # 'tag': forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
            #                                       # choices=Tag.objects.all(),
            #                                       queryset=Tag.objects.all(),
            #                                       ),
        }


class CreateComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Leave a comment',
                                             'aria-label': 'Leave a comment'}), }
