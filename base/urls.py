from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('account/', views.account, name="account"),
    path('account/delete/', views.deleteAccountModal, name="deleteAccount"),
    path('account/confirm-delete/', views.deleteUser, name="confirmDeleteAccount"),
    path('account/change-password/', views.changePassword, name="changePassword"),
    path('account/upload-profile-picture/', views.uploadProfilePicture, name="uploadProfilePicture"),
    path('new/', views.createFile, name="createFile"),
    path('<str:pk>/delete/', views.deleteFile, name="deleteFile"),
    path('files/<str:pk>/view/', views.viewFileText, name="viewFileText"),
    path('files/', views.files, name="files"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)