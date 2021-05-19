# from django.contrib import admin
from django.urls import path

from authentication.views import LoginView, RegisterView, ApiRoot, UserList
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ApiRoot.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('list/', UserList.as_view(), name='list'),
    path('login/', LoginView.as_view(), name='login'),

    # path('admin/', admin.site.urls),
]


urlpatterns = format_suffix_patterns(urlpatterns)
