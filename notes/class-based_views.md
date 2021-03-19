# Class-based views
Las vistas también pueden ser clases, que tienen el objetivo de evitar la repetición de tareas como mostrar los templates, son vistas genéricas que resuelven problemas comunes. 
Son vistas genéricas que suelen resolver problemas muy comunes como validar formularios, cargar un template...

Documentación: https://docs.djangoproject.com/en/3.1/topics/class-based-views/

Página recomendada: https://ccbv.co.uk/
Permite ver documentación sobre esto con funciones útiles

También es recomendable mover las Urls a cada una según su app 
 usando include en los Paths quedando tal que 

```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static  
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
                  path('', include(('posts.urls', 'posts'), namespace='posts')),
                  path('users/', include(('users.urls', 'users'), namespace='users')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Y el archivo donde se guardan todas las urls de la app incluida seria

```python
# Users.urls
from django.urls import path
from django.views.generic import TemplateView

from learning.users import views

urlpatterns = [

    path(
        route='<str:username>/',
        view=TemplateView.as_view(template_name='users/detail.html'),
        name='detail'
    ),

    path(
        route='users/login/',
        view=views.login_view,
        name='login'
    ),

    path(
        route='users/logout/',
        view=views.logout_view,
        name='logout'
    ),

    path(
        route='users/singup/',
        view=views.singup_view,
        name='singup'
    ),

    path(
        route='users/me/profile/',
        view=views.update_profile,
        name='update_profile'
    )

]

```

En el código de arriba se puede ver como queda con el class-based view predefinido por Django

Cuando modifiques las url te tocará hacerlo también en el HTML de la siguiente forma
- Enviar con algún parámetro
```html
 <a href="{% url 'users:detail' request.user.username">
```
- De forma estándar
```html
 <a href="{% url 'users:logout'%}">
```

## Proteger Generic Class Views
Personalizándolo, simplemente crea una clase en views que herede de la generic class y añade campos y validaciones según sea necesario

```python
# DetailView

# Para hacerlo LoginRequired
from django.contrib.auth.mixins import LoginRequiredMixin

# Generic Class View a usar
from django.views.generic import DetailView

# Models
from django.contrib.auth.models import User
from  learning.posts.models import Post


class UserDetailView(DetailView, LoginRequiredMixin):
    # User Detail View
    template_name = 'users/detail.html'
    slug_field = 'username' # Como se hara en la queryset
    slug_url_kwarg = 'username' # Como sera llamado desde la URL
    model = User
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add Users Post to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context
```
```python
#Using Create View
class CreatePostView(LoginRequiredMixin, CreateView):
    # Create a New Post
    template_name = "posts/new.html"
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        # Add User and profile to context #
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
```
```python
# Using FormView
class SingupView(FormView):
    # Sing up view
    template_name = "users/singup.html"
    form_class = SingupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Save form data
        form.save()
        return super().form_valid(form)
```

```python
# Using UpdateView
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    # Log in view
    template_name = 'users/update/profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'profile_picture']


    def get_object(self, queryset=None):
        # Return users profile if
        return self.request.user.profile

    def get_success_url(self):
        # Return to Users Profile
        username = self.object.user.username
        return reverse('users:detail', kwargs= {'username': username})
```
```python
# Using List View
class PostsFeedView(LoginRequiredMixin, ListView):
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'
```

## Login y Logout views
Son de las mas sencillas solo tienes que heredar de ellas y añadirle el redirect link en el archivo settings y el 
template

```python
# users/views.py

from django.contrib.auth import views as auth_views

class LoginView(auth_views.LoginView):
    # Login View
    template_name = 'users/login.html'
    
    # Esto es para que si un user ya esta autenticado lo redirige a posts
    redirect_authenticated_user = True

class LogoutView(auth_views.LogoutView):
    # Log out View
    pass
```
```python
# Settings.py

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/posts/"
LOGOUT_REDIRECT_URL = LOGIN_URL
```