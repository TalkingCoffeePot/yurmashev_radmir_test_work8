from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import UserRegisterView, logout_view, UserProfile, UserProfileEdit, ReviewEdit, ReviewDelete, ModerateReviewDelete, ModerateReviewEdit, UserPasswordChangeView

app_name='accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='log_in'),
    path('logout/', logout_view, name='log_out'),
    path('create/', UserRegisterView.as_view(), name='register_user'),
    path('<int:user_pk>', UserProfile.as_view(), name='profile'),
    path('<int:user_pk>/edit/', UserProfileEdit.as_view(), name='profile_edit'),
    path('<int:user_pk>/edit/password_change/', UserPasswordChangeView.as_view(), name='password_edit'),
    path('<int:user_pk>/review_edit/<int:review_pk>/', ReviewEdit.as_view(), name='review_edit'),
    path('<int:user_pk>/review_delete/<int:review_pk>/', ReviewDelete.as_view(), name='review_delete'),
    path('moderate/review_edit/<int:review_pk>/', ModerateReviewEdit.as_view(), name='review_edit_moderate'),
    path('moderate/review_delete/<int:review_pk>/', ModerateReviewDelete.as_view(), name='review_delete_moderate')
]