"""dj_reff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from entries.views import landing_page, LandingPageView, SignupView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from entries.views import EntryDetailShortURLView, TestingView, EntryFillView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('testing/', TestingView.as_view(), name='testing'),
    # Change the URL .py folder from global to app-specific ('entries' in our case)
    path('entries/', include('entries.urls', namespace="entries")),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page="landing-page"), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # the following path needs to specify the uid in base64 and the token for a successful password reset
    path('password-confirm-done/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('fill-<str:short_url>/', EntryFillView.as_view(), name='entry-fill'),
    # the following path needs to stay last, otherwise the it would raise an error
    path('<str:short_url>/', EntryDetailShortURLView.as_view(),
         name='entry-detail-short-url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
