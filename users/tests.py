from django.test import TestCase
# from users.models import Profile
from django.contrib.auth.models import User

class UserTest(TestCase):
    
    def create_user(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.client.login(username='testuser1', password='12345')
        return User.objects.get(id=1)
    
    def test_profile_model(self):
        # self.user = User.objects.create_user(username='testuser', password='12345')
        # # self.client.login(username='testuser', password='12345')
        self.user = self.create_user()
        self.assertEqual(self.user.username+' Profile', self.user.profile.__str__())
    

# Create your tests here.
