# Django

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from posts.forms import PostForm

from posts.models import Post


# Create your views here.
"""
 DEPRECATED VIEWS 

def list_posts_html_plain(request):
    # List of existing posts 
    content = []
    for post in posts:
        # por cada post en el diccionario generamos un html
        content.append(f'''
            <p><strong>{post['name']}</strong></p>
            <p><small>{post['user']} - <i>{post['timestamp']}</i></small></p>
            <figure><img src="{post['picture']}"/></figure>
        ''')
    return HttpResponse('<br>'.join(content))  # Inyectamos el Html hecho separado por el <br>


@login_required
def list_posts(request):
    # retorna el request, un template y un contexto, que es un diccionario
    posts = Post.objects.all().order_by('created')
    profile = request.user.profile
    return render(request, 'posts/feed.html', {'posts': posts})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            form.save()
            return redirect("posts:feed")
    else:
        form = PostForm()

    return render(
        request=request,
        template_name='posts/new.html',
        context={
            'form': form,
            'user': request.user,
            'profile': request.user.profile
        }
    )

DEPRECATED
"""


class PostsFeedView(LoginRequiredMixin, ListView):
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 30
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = "posts/detail.html"
    queryset = Post.objects.all()
    context_object_name = 'post'

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