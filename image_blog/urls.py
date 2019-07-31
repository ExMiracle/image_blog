from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import include
from users import views as user_views
#from users.views import FriendView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', user_views.register, name='register'),
    path('user/<str:username>/', user_views.ProfileView.as_view(), name = 'profile'),
    path('edit/', user_views.profile, name='profile-edit'),
    path('user/<str:username>/follow', user_views.FollowRedirectView.as_view(), name = 'follow'),
    path('api/user/<str:username>/follow', user_views.PostFriendAPIView.as_view(), name = 'api-follow'),
#    path('user/<str:username>/friend/', user_views.FriendView.as_view(), name = 'friends'),
#    path('user/<str:username>/friend/', user_views.making_friends, name='friends'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
            template_name = 'users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name = 'users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name = 'users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
            template_name = 'users/password_reset_complete.html'), name='password_reset_complete'),
    path('blog/comments/', include('fluent_comments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
