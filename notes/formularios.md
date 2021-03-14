# Formularios en Django
Se puede trabajar perfectamente con HTML pero Django trae su propia clase para implementarlos directamente heredando de esta
```python
from django import forms

class NombreFormulario(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100)
```
Luego puedes añadir estos formularios directamente a las views en la que haga falta

```python
from django.shortcuts import render, redirect

from .forms import UpdateUser

def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        print(request.POST)
        form = UpdateUser(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.biography = data['biography']
            profile.phone_number = data['phone_number']
            profile.profile_picture = data['picture']

            profile.save()
            
            return redirect('update_profile')
    else:
        form = UpdateUser()
    return render(
        request,
        'users/update/profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
        )
```
La clase utilitaria para formularios de Django nos ayuda a resolver mucho del trabajo que se realiza de forma repetitiva. La forma de implementarla es muy similar a la implementación de la clase models.model.

Algunas de las clases disponibles en Django al implementar form, son:

- BooleanField
- CharField
- ChoiceField
- TypedChoiceField
- DateField
- DateTimeField
- DecimalField
- EmailField
- FileField
- ImageField
- URLField

Para añadir mensajes de error y elementos de Django dentro del HTML del Formulario puedes hacerlo perfectamente

```html
 <input
                        class="form-control {% if form.website.errors %}is-invalid{% endif %}"
                        type="url"
                        name="website" placeholder="Website"
                        value="{{profile.website}}"
                    />
```

Tambien existen las Model Forms las cuales lee segun los campos definidos por el modelo dado, declarando el modelo y los fields  a usar de las sihuente forma

```python
""" Posts forms """
# Django
from django import forms
# Models
from posts.models import Post

class PostForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = ("user", "profile", "title", "photo")
```

Si quieres que los datos se muestren en Admin recuerda declararlos en Admin.py

```python
from django.contrib import admin
from posts.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'photo', )

admin.site.register(Post, PostAdmin)
```