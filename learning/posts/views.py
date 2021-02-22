# Django
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render  # Toma un request

posts = [
    {
        'title': "Peter Chiguire",
        'user': {
            'name': "@PeterChig",
            'picture': "https://ih1.redbubble.net/image.917912217.1975/flat,128x128,075,t-pad,128x128,f8f8f8.jpg"
        },
        'timestamp': datetime.now().strftime("%a %d/%m/%Y - %H:%M"),
        'photo': "https://www.venezuelatuya.com/natura/imagenes/047chiguire3.jpg"

    },
    {
        'title': "Chiguires in love",
        'user': {'name': "@PeterChigInLove",
                 'picture': "https://64.media.tumblr.com/avatar_e3311873a30d_128.pnj"
                 },
        'timestamp': datetime.now().strftime("%a %d/%m/%Y - %H:%M"),
        'photo': "https://www.venezuelatuya.com/natura/imagenes/047chiguire2.jpg"
    },
    {
        'title': "Fachero el Chiguire",
        'user': {'name': "@FachaChig",
                 'picture': "https://ih1.redbubble.net/image.870527524.5159/flat,128x128,075,t-pad,128x128,f8f8f8.jpg"
                 },
        'photo': "https://agenciameme.com/wp-content/uploads/2020/05/capibaras-758x506.jpg",
        'timestamp': datetime.now().strftime("%a %d/%m/%Y - %H:%M")

    }
]


# Create your views here.
def list_posts_html_plain(request):
    """List of existing posts"""
    content = []
    for post in posts:
        # por cada post en el diccionario generamos un html
        content.append(f"""
            <p><strong>{post['name']}</strong></p>
            <p><small>{post['user']} - <i>{post['timestamp']}</i></small></p>
            <figure><img src="{post['picture']}"/></figure>
        """)
    return HttpResponse('<br>'.join(content))  # Inyectamos el Html hecho separado por el <br>


def list_posts(request):
    # retorna el request, un template y un contexto, que es un diccionario
    return render(request, 'feed.html', {'posts': posts})
