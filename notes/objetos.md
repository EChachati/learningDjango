# Objetos
## Request
Es la solicitud generada en el url
### Metodos
- GET que en el URL es con '?' por ejemplo para enviar un texto con una cadena de numeros seria:
  ```
  http://localhost:8000/example?number=10,4,50,32
  ```

## HttpResponse
Enviar respuestas a los request usando el protocolo HTTP
## JsonResponse
Enviar respuestas a los request usando el formato JSON
#### Parametros
- data: primer parametro, la información a enviar en JSON 
- safe: False cuando envies un objeto que no sea un diccionario de python, por defecto en True 
## render
Se usa para enviar una página como tal, es decir un renderizado de un HTML element
#### Parametros
- request: El Mismo request que fuen enviado Primer Parametro
- Template: El Archivo HTML
