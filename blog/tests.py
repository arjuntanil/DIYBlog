from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blogger, BlogPost, Comment, Poll, PollOption

# Create your tests here.

class BloggerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio',
            phone_number='1234567890'
        )

    def test_blogger_str(self):
        self.assertEqual(str(self.blogger), 'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(
            self.blogger.get_absolute_url(),
            reverse('blogger-detail', args=[str(self.blogger.id)])
        )

class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.blog_post = BlogPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.blogger
        )

    def test_blog_post_str(self):
        self.assertEqual(str(self.blog_post), 'Test Post')

    def test_get_absolute_url(self):
        self.assertEqual(
            self.blog_post.get_absolute_url(),
            reverse('blog-detail', args=[str(self.blog_post.id)])
        )

class BlogListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio'
        )
        number_of_posts = 6
        for post_num in range(number_of_posts):
            BlogPost.objects.create(
                title=f'Test Post {post_num}',
                content='Test content',
                author=self.blogger
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blogs'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['blogpost_list']), 5)

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.blog_post = BlogPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.blogger
        )
        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            author=self.user,
            content='Test comment'
        )

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'Test comment')

class PollTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio'
        )
        self.blog_post = BlogPost.objects.create(
            title='Test Post',
            content='Test content',
            author=self.blogger
        )
        self.poll = Poll.objects.create(
            blog_post=self.blog_post,
            question='Test question?'
        )
        self.poll_option = PollOption.objects.create(
            poll=self.poll,
            option_text='Test option'
        )

    def test_poll_str(self):
        self.assertEqual(str(self.poll), 'Test question?')

    def test_poll_option_str(self):
        self.assertEqual(str(self.poll_option), 'Test option')
