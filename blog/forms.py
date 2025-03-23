from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Comment, BlogPost, Blogger

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            blogger = Blogger.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                bio=self.cleaned_data['bio']
            )
        return user

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'is_protected', 'password', 'audio_file']
        widgets = {
            'password': forms.PasswordInput(),
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            if audio_file.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError('Audio file must be less than 10MB')
            
            if not audio_file.content_type.startswith('audio/'):
                raise ValidationError('Please upload a valid audio file')
            
            self.instance.has_audio = True
        return audio_file

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.has_audio = bool(instance.audio_file)
        if commit:
            instance.save()
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class PasswordProtectedPostForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class BloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = ['bio', 'phone_number', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
