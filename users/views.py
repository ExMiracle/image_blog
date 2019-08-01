from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from .models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.views.generic import DetailView, RedirectView, ListView, View

    
class TryView(View):
    model = Profile
    
    def friend_check(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        profile = Profile.objects.get(user=user)
        follower_list = self.request.user.profile.get_following()
        if profile in follower_list:
            return "Unfollow"
        else:
            return "Follow"

    def get_context_data(self, **kwargs):
        context = super(TryView, self).get_context_data(**kwargs)
        if self.friend_check() == "Unfollow":
            context['color'] = 'btn-info'
        else:
            context['color'] = 'btn-outline-info'
        return context

class ProfileView(TryView, DetailView):
    template_name = 'users/profile.html'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
    
    def get_user(self):
        if self.request.user is None:
            return None
        return self.request.user
    
class ProfileFollowerView(TryView, ListView):
    template_name = 'users/followers.html' # <app>/<model?_<viewtype>.html
    context_object_name = 'followers'
    paginate_by = 50
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.get(user=user).get_followers()
    
class ProfileFollowingView(TryView, ListView):
    template_name = 'users/following.html' # <app>/<model?_<viewtype>.html
    context_object_name = 'following'
    paginate_by = 50
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.get(user=user).get_following()    





#class ProfileView(DetailView):
#    model = Profile
#    template_name = 'users/profile.html'
#    
#    def get_object(self):
#        return get_object_or_404(User, username=self.kwargs.get('username'))
#    
#    def get_user(self):
#        if self.request.user is None:
#            return None
#        return self.request.user
#    
#    def friend_check(self):
#        user = get_object_or_404(User, username=self.kwargs.get('username'))
#        profile = Profile.objects.get(user=user)
#        follower_list = self.request.user.profile.get_following()
#        if profile in follower_list:
#            return "Unfollow"
#        else:
#            return "Follow"
#
#    def get_context_data(self, **kwargs):
#        context = super(ProfileView, self).get_context_data(**kwargs)
#        if self.friend_check() == "Unfollow":
#            context['color'] = 'btn-info'
#        else:
#            context['color'] = 'btn-outline-info'
#        return context
#
#class ProfileFollowerView(ListView):
#    model = Profile
#    template_name = 'users/followers.html' # <app>/<model?_<viewtype>.html
#    context_object_name = 'followers'
#    paginate_by = 50
#    
#    def get_queryset(self):
#        user = get_object_or_404(User, username=self.kwargs.get('username'))
#        return Profile.objects.get(user=user).get_followers()
#    
#        
#class ProfileFollowingView(ListView):
#    model = Profile
#    template_name = 'users/following.html' # <app>/<model?_<viewtype>.html
#    context_object_name = 'following'
#    paginate_by = 50
#    
#    def get_queryset(self):
#        user = get_object_or_404(User, username=self.kwargs.get('username'))
#        return Profile.objects.get(user=user).get_following()

class FollowRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        n_f = get_object_or_404(User, username=self.kwargs.get('username'))
        owner = self.request.user.profile
        new_friend = Profile.objects.get(user=n_f)
        url_ = new_friend.get_absolute_url()
        if new_friend in owner.get_following():
            owner.remove_relationship(new_friend, 1)
        else:
            owner.add_relationship(new_friend, 1)
        return url_

class PostFriendAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, username=None, format=None):
        n_f = get_object_or_404(User, username=username)
        owner = self.request.user.profile
        new_friend = Profile.objects.get(user=n_f)
        updated = False
        friended = False
        if new_friend in owner.get_following():
            friended = False
            owner.remove_relationship(new_friend, 1)
        else:
            friended = True
            owner.add_relationship(new_friend, 1)
        updated = True
        data = {
            "updated": updated,
            "friended": friended
        }
        return Response(data)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
            'u_form': u_form,
            'p_form': p_form 
    }
    return render(request, 'users/profile-edit.html', context)
