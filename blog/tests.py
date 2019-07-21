from django.test import TestCase
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.test import override_settings

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')


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
        
    def test_post_creation(self, url='/post/new/'):
        self.create_user()
        data = {'title':'title',
                'content':'Post'}
        try_post = self.client.post(url, data)
        self.assertRedirects(try_post, '/post/1/')
    
    def test_post_model(self):
        self.post = self.create_post()
        # new_post = self.create_post()
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.title, self.post.__str__())        
    
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_about_status_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('blog-about'))
        self.assertEqual(response.status_code, 200)
    
    def test_new_post_status_code(self):
        self.create_user()
        response = self.client.get('/post/new/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)