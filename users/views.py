from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
#from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile

#from .forms import ButtonForm
#from django.http import JsonResponse

from django.views.generic import DetailView, RedirectView
#from django.views import View







class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
    
    def get_user(self):
        if self.request.user is None:
            return None
        return self.request.user
    
class FollowRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        n_f = get_object_or_404(User, username=self.kwargs.get('username'))
        owner = self.request.user.profile
        new_friend = Profile.objects.get(user=n_f)
        url_ = new_friend.get_absolute_url()
#        updated = False
#        friended = False
        if new_friend in owner.get_following():
            owner.remove_relationship(new_friend, 1)
#            friended = False
        else:
            owner.add_relationship(new_friend, 1)
#            friended = True
#        updated = True
#        data = {
#                'updated': updated,
#                'friends': friended,
#                'url': url_
#        }
#        return JsonResponse(data)
        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostFriendAPIView(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, username=None, format=None):
        # slug = self.kwargs.get("slug")
#        obj = get_object_or_404(Post, slug=slug)
#        url_ = obj.get_absolute_url()
#        user = self.request.user
        
#        n_f = get_object_or_404(User, username=self.kwargs.get('username'))
        n_f = get_object_or_404(User, username=username)
        owner = self.request.user.profile
        new_friend = Profile.objects.get(user=n_f)
#        url_ = new_friend.get_absolute_url()
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
            return redirect('profile')
#            return redirect({{ profile.get_absolute_urls }})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
            'u_form': u_form,
            'p_form': p_form 
    }
    
    return render(request, 'users/profile-edit.html', context)
# Create your views here.
