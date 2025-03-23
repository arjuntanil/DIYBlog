from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from .models import BlogPost, Comment, Blogger, Like
from .forms import BlogPostForm, CommentForm, BloggerForm, ExtendedUserCreationForm

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 10

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comment_set.all().order_by('-created_date')
        
        # Check if user has access to password-protected post
        if self.object.is_protected:
            context['has_access'] = self.request.session.get(f'post_access_{self.object.pk}', False)
        else:
            context['has_access'] = True
            
        if self.request.user.is_authenticated:
            context['user_has_liked'] = self.object.is_liked_by(self.request.user)
        return context

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            blogger = Blogger.objects.get(user=request.user)
            post.author = blogger
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog-detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})

@login_required
def update_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # Check if user is the author
    if request.user != post.author.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('blog-detail', pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # If no new audio file is uploaded, keep the existing one
            if not request.FILES.get('audio_file') and post.audio_file:
                form.instance.audio_file = post.audio_file
                form.instance.has_audio = True
            
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog-detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/update_blog_post.html', {
        'form': form,
        'blogpost': post
    })

@login_required
def delete_blog_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author.user != request.user:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('blog-detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blog-list')
    return render(request, 'blog/delete_blog_post.html', {'post': post})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
    return redirect('blog-detail', pk=pk)

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
    
    return JsonResponse({
        'success': True,
        'likes_count': post.likes.count(),
        'is_liked': created
    })

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to DIY Blog.')
            return redirect('blog-list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExtendedUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

class BloggerListView(ListView):
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'bloggers'

    def get_queryset(self):
        return Blogger.objects.annotate(
            total_likes=Count('blogpost__likes'),
            post_count=Count('blogpost')
        ).filter(post_count__gt=0).order_by('-total_likes')

class BloggerDetailView(DetailView):
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogger = self.get_object()
        posts = BlogPost.objects.filter(author=blogger).order_by('-created_date')
        context['posts'] = posts
        context['total_posts'] = posts.count()
        context['total_likes'] = Like.objects.filter(post__author=blogger).count()
        return context

def check_post_password(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        password = request.POST.get('password')
        if post.password == password:
            request.session[f'post_access_{post.pk}'] = True
            messages.success(request, 'Access granted!')
        else:
            messages.error(request, 'Incorrect password!')
    return redirect('blog-detail', pk=pk)
