# Templates
## Añadir al proyecto
Primero que nada debemos crear la carpeta donde tendremos los Templates en el proyecto, fuera de las apps y declararlos en settings.py
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Adding Templates directory
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
Ahora Django vera los folders en ese array y ahora una buena práctica es sacar los templates de las apps y guardarlos en subcarpetas dentro de la carpeta 'templates'

allí iremos poniendo varios archivos HTML y templates para inyectar en otros, usando la lógica de Django en HTML

```html
{% block nombre_bloque %}
    <!-- Bloque contenedor con el que se va a inyectar el HTML deseado, se declara igual para el que inyecta como el que será inyectado-->
{% endblock %}

{{ post.user.name }} <!--Añadir el valor desde post.user.name-->

{% extends 'base.html' %} <!-- Indicar aque archivo va a inyectar el HTML -->

{% include "nav.html" %} <!--Inyectar un archivo HTML completo-->


<link rel="stylesheet" href="{% static 'css/main.css' %}" /> 
<!--Traer algo de la carpeta Static-->
```
Para que acepte los statics debemos modificar el settings.py
 y añadir la siguiente linea con el path de la carpeta static
 ```python
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

## Login
Se utiliza el Middleware de Sessions dentro del User Authentication de Django, el cual se encarga de validar toda la sesión de un user, y se importa lo necesario y con la request y atributo POST se puede autenticar de la siguente forma

```python
from django.contrib.auth importh authenticate, login

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(
        request,
        username=username,
        password=password
        )
    if user is not None:
        login(request, user)
        # Redirect to a Success page
    else:
        # Return to an 'invalid login' error message
```

En el HTML cada vez que hagas uso de un POST debes colocar el atributo especial de Django
```HTML
{% csrf_token %}
```
Para señalizar un error se debe retornar un render igual pero añadiendo el contexto del error asi
```python
return render(request, 'users/login.html', context={'error':'Invalid user or password'})
```
Y añadir en el HTML el siguiente condicional o uno similar dentro del block
```HTML    
{% if error %}
    <p style="color: red;">{{ error }}</p>
{% endif %}
```
Y si para una función es necesario que el user este loggeado usa el decorator
```python
@login_required
def view(request):
    # Function Code
```
Si no esta loggeado lo redirecciona a settings.LOGIN_URL, por lo que se debe modificar ese valor tal que por ejemplo
```python
LOGIN_URL = "/users/login/"
```
# Log Out
Hacer un Logout es bastante sencillo, es colocar la URL deseada dentro del redireccionamiento con el HTML
```HTML
<li class="nav-item nav-icon">
    <a href="{% url 'logout'%}">
        <i class="fas fa-sign-out-alt"></i>
    </a>
</li>
```
Añadir el Url deseado y crear la vista que redireccione y haga el logout
```python
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
```

### NOTA: 
    Usar decorator @login_required para evitar un logout de alguien que no esta loggeado 

# Sing Up
Para crear un Sing Up, debes crear primero el archivo HTML respectivo, con los campos necesarios, de forma muy similara al del login

Luego debes añadir el URL y la funcion respectiva en urls.py

Y finalmente crear la funcion en views tal que valides además los campos necesarios

```python
    def singup_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']
            confirmedpassword = request.POST['confirmpassword']
            email = request.POST['email']

            # Validate Password
            if password != confirmedpassword:
                return render(
                    request,
                    'users/singup.html', 
                    context={'error': 'Passwords do not match'}
                    )

            # Validate Username is not already taken
            if User.objects.filter(username=username):
                return render(
                    request, 
                    'users/singup.html', 
                    context={'error': 'Username is already taken'}
                    )
            
            # Creates User with data from POST
            u = User.objects.create_user(
                username=username,
                email=email,
                password=password
                )
            u.first_name = first_name
            u.last_name = last_name
            u.save()

            # Create the profile using User
            profile = Profile(user=u)
            profile.save()
            return redirect('feed')

        return render(request, 'users/singup.html')
```

# Middlewares
Es una serie de Hooks y una API d ebajo nivel que nos permite modificar el objeto request antes de que llegue a la vista y response antes que salga de la vista

Un Middleware puede crearse en cualquier parte pero lo mas recomendable es que este en la aplicación en la que se usa, pero en caso de que haya middlewares comunes, lo mejor es tenerlos en una carpeta aparte

Estos Middlewares se ejecutan en el orden en el que estan declarados en su sección respectiva en settings.py, ya hay varios por defecto:

- ### SecurityMiddleware: 
    Se encarga de comprobar todas las medidas de seguridad, las variables de settings relacionadas con Https, Auth, entre otros.
- ### SessionMiddleware: 
    Se encarga de validar una sesión.
- ### CommonMiddleware: 
    Se encarga de verificar componentes comunes como lo que es del debug.
- ### CsrfViewMiddleware: 
    Se encarga de toda la validación correspondiente a CSRF. Éste nos permite utilizar el tag {% csrf_token %} y es el que inserta el token de seguridad en cada formulario.
- ### AuthenticationMiddleware: 
    Nos permite agregar request.user o users anónimos desde las vistas.
- ### MessageMiddleware:
    Pertenece al Framework de mensajes de Django, y permite pasar un mensaje sin necesidad de mantener un estado en la base de datos o en memoria.
- ### XFrameOptionsMiddleware: 
    Middleware de seguridad.

Ahora vamos a crear un middleware para modificar los datos del Profile apenas se registre un user

Añadimos la url en urls.py
```python
path(
    'users/me/profile/', 
    users_views.update_profile, 
    name='update_profile'
    )
```
Aqui ya hay que crear el Middleware con una clase de la siguente forma 
```python
# Django Imports
from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """
    Ensure every user using the platform has all his profile data complete
    Including profile picture, bio, phone number, etc. 
    """
    def __init__(self, get_response):
        # Middleware Initialization 
        self.get_response = get_response
    
    def __call__(self,request):
        # Code to be executed for each request before de view is called

        if not request.user.is_anonymous:
            if request.path not in [reverse('update_profile'), reverse('logout')]: # If i'm not already in that link or in logout
                # calling a OneToOneField
                profile = request.user.profile
                if not profile.profile_picture or not profile.biography:
                    return redirect('update_profile')
        else:
            if request.path != reverse('login'): # If i'm not already in that link
                return redirect('login')
        response = self.get_response(request)
        return response
```
Instalamos el Middleware en settings.py añadiendolo al final de la lista de middlewares y ya esta funcionando