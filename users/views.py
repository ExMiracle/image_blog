from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Profile
#from . import models
from django.views.generic import DetailView

class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
    
    def get_user(self):
        if self.request.user is None:
            return None
        return self.request.user
        

@login_required
def making_friends(request, username, status):
    n_f = get_object_or_404(User, username=username)
    owner = request.user.profile
    new_friend = Profile.objects.get(user=n_f)

    if status == 1:
        owner.add_relationship(new_friend, RELATIONSHIP_FOLLOWING)
    else:
        owner.remove_relationship(new_friend, RELATIONSHIP_FOLLOWING)

    return redirect('friend_page.html')
#    pass



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
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
            'u_form': u_form,
            'p_form': p_form 
    }
    
    return render(request, 'users/profile-edit.html', context)
# Create your views here.

