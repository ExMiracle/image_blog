from django.test import TestCase
from users.models import Profile
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.uploadedfile import SimpleUploadedFile

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')


class UserTest(TestCase):
    
    def create_user(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.client.login(username='testuser1', password='12345')
        return User.objects.get(id=1)
    
    def test_valid_user_update_form(self):
        self.create_user()
        data = {'username':'UserName',
                'email':'email@email.com'}
        form = UserUpdateForm(data=data)
        self.assertTrue(form.is_valid())
        
    def test_profile_model(self):
        self.create_user()
        self.assertEqual(self.user.username+' Profile', self.user.profile.__str__())
    
    def test_profile_view(self):
        self.create_user()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'users/profile.html')
        self.failUnless(isinstance(response.context['p_form'],
                                   ProfileUpdateForm))
        self.failUnless(isinstance(response.context['u_form'],
                                   UserUpdateForm))
    
    def test_profile_view_post_success(self):
        self.create_user()
        data = {'username':'UserName',
              'email':'email@email.com'}
        image = SimpleUploadedFile("file.jpeg", b"file_content", content_type="image/jpeg")
        u_form = UserUpdateForm(data=data)
        p_form = ProfileUpdateForm(data=image)
        self.assertTrue(u_form.is_valid())
        self.assertTrue(p_form.is_valid())
        response = self.client.post(reverse('profile'),
                                    data={'username':'UserName',
                                          'email':'email@email.com',
                                          'image':'image.jpeg'})
        self.assertRedirects(response, '/profile/')
        
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'users/register.html')
        self.failUnless(isinstance(response.context['form'],
                                   UserRegisterForm))
    
    def test_register_view_post_success(self):
        data = {'username':'UserName',
              'email':'email@email.com',
              'password1':'Testing321',
              'password2':'Testing321'}
        form = UserRegisterForm(data=data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('register'), data=data)
        self.assertRedirects(response, '/login/')
        self.assertEqual(Profile.objects.count(), 1)