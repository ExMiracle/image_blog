from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')
    
    def get_absolute_url(self):
        username = User.objects.get(username=self.user).username
        return reverse('profile', args=[username])

    def get_following_url(self):
        username = User.objects.get(username=self.user).username
        return reverse('profile-following', args=[username])
    
    def get_followers_url(self):
        username = User.objects.get(username=self.user).username
        return reverse('profile-followers', args=[username])
    
    def get_username(self):
        return self.user.username
    
    def follow_check(self, person):
        follower_list = self.get_following()
        if person in follower_list:
            return "Unfollow"
        else:
            return "Follow"
        
#    def get_friend_url(self):
#        username = User.objects.get(username=self.user).username
#        return reverse('follow', args=[username])
#    
#    def get_api_friend_url(self):
#        username = User.objects.get(username=self.user).username
#        return reverse('api-follow', args=[username])
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def add_relationship(self, person, status):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return relationship

    def remove_relationship(self, person, status):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return
    
    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__from_person=self)
    
    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self)
    
    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)
    
    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)


RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)

class Relationship(models.Model):
    from_person = models.ForeignKey(Profile, related_name='from_people',
                                    on_delete = models.CASCADE)
    to_person = models.ForeignKey(Profile, related_name='to_people',
                                  on_delete = models.CASCADE)
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
