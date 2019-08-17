"""calorieTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from trackerUser.views import CreateUser, UpdateUser, DeleteUser, GetUser
from tracker.views import AddEntry, UpdateEntry, DeleteEntry, GetEntries

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^user/create/$', CreateUser.as_view(), name='create_user'),
    url(r'^user/update/$', UpdateUser.as_view(), name='update_user'),
    url(r'^user/delete/$', DeleteUser.as_view(), name='delete_user'),
    url(r'^user/get/$', GetUser.as_view(), name='get_user'),
    url(r'^entry/create/$', AddEntry.as_view(), name='add_entry'),
    url(r'^entry/update/$', UpdateEntry.as_view(), name='update_entry'),
    url(r'^entry/delete/$', DeleteEntry.as_view(), name='delete_entry'),
    url(r'^entry/get/$', GetEntries.as_view()),
    # url(r'^entry/delete/$'),
    # url(r'^calories/analytics/$'),
]
