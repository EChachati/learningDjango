"""learning URL Configuration

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
from django.contrib import admin
from django.urls import path

from learning import views as local_views
from posts import views as posts_views

urlpatterns = [
    # path("url", funcion_que_ejecuta)
    path('hello-world/', local_views.hello_world),
    path('sorted_numbers/', local_views.sorted_numbers),
    # Use <str:name> to send a parameter to be used in the url
    path('hi/<str:name>/<int:age>/', local_views.say_hi),
    path('posts_plain/', posts_views.list_posts_html_plain),
    path('posts/', posts_views.list_posts),
    path('admin/', admin.site.urls)
]
