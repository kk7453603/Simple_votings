"""simple_votings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from main import views
from django.contrib.auth import views as auth_views

from django_registration.backends.one_step.views import RegistrationView
from main.forms import CustomRegistrationForm
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from main.views import get_menu_context

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('votings/', views.voting_list_page, name='votings'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            extra_context={
                'menu': get_menu_context(),
                'pagename': 'Авторизация'
            }
        ),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('voting/<int:pk>/', views.voting_page, name='voting'),
    path('accounts/register/',
        RegistrationView.as_view(
            form_class=CustomRegistrationForm
        ),
        name='django_registration_register',
    ),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('voting/<int:pk>/complaint/', views.complaint_page, name='voting_complaint'),
    path('voting/<int:pk>/editing/', views.voting_editing_page, name='voting_editing'),
    path('creating/', views.voting_creation_page, name='voting_create'),
    path('complaint_list/', views.complaint_list_page, name='complaint_list'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/editing/', views.profile_editing_page, name='profile_editing'),
]
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
