# "request" parametro por defectos en las funciones de Django
from django.http import HttpResponse, QueryDict, JsonResponse

from datetime import datetime


def hello_world(request):
    now = datetime.now().strftime("%a %d/%m/%Y - %H:%M")
    return HttpResponse(f"hello world, the current server time is {now}")


def sorted_numbers(request):
    import pdb  # Esto es un debugger, te permite acceder a los estados de los objetos por consola.
    pdb.set_trace()  # Marca debuuger
    lista = request.GET.get("number", [0]).split(",")
    lista = sorted(int(element) for element in lista)
    data = {
        'status': 'ok',
        'numbers': lista,
        'message': "niqqa it works"
    }
    return JsonResponse(data)  # Safe = False en caso de que envies un objeto que no sea un dict


def say_hi(request, name, age):
    if age > 13:
        return HttpResponse(f"Hi {name}! Welcome you are {age} years old")
    return HttpResponse(f"Sorry {name} you can't come, you are only {age} years old")
