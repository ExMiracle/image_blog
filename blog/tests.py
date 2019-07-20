from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# from django.core.urlresolvers import reverse
# from blog.forms import WhateverForm

from django.test import override_settings
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')


# models test
class PostTest(TestCase):
    
    def create_user(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        return User.objects.get(id=1)
    
    def create_post(self, title="only a test",
                    content="yes, this is only a test"):
        return Post.objects.create(title=title,
                                   content=content,
                                   author=self.create_user(),
                                   date_posted=timezone.now())

    def test_post_creation(self):
        new_post = self.create_post()
        self.assertTrue(isinstance(new_post, Post))
    
    def test_post_model(self):
        self.post = self.create_post()
        self.assertEqual(self.post.title, self.post.__str__())
    
    
    def test_valid_user_register_form(self):
        data = {'username':'UserName',
                'email':'email@email.com',
                'password1':'12345',
                'password2':'12345'}
        form = UserRegisterForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_valid_user_update_form(self):
        data = {'username':'UserName',
                'email':'email@email.com'}
        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_reverse_home_url_status_code(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        
    def test_about_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_reverse_about_status_code(self):
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
    
        
    # def test_post_list_view(self):
    #     # w = self.create_whatever()
    #     url = reverse("PostListView.as_view()")
    #     resp = self.client.get(url)

    #     self.assertEqual(resp.status_code, 200)
        # self.assertIn(w.title, resp.content)
        
    # def test_home_page(self, context={'posts': Post.objects.all()}):
    #     url = reverse("blog.views.home")
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, 200)

        
