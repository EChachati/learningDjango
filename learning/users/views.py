# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Forms
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, FormView, UpdateView
from users.forms import SingupForm

# Models
from django.contrib.auth.models import User
from users.models import Profile

from  posts.models import Post



def login_view(request):
    if request.method == 'POST':
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
            return redirect('posts:feed')
        else:
            # Return to an 'invalid login' error message
            return render(request, 'users/login.html', context={'error': 'Invalid user or password'})
    #    import pdb
    #    pdb.set_trace()
    return render(
        request,
        template_name='users/login.html'
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')

""" DEPRECATED
def singup_view(request):
    if request.method == 'POST':

        form = SingupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')

        else:
            form = SingupForm()
        return render(request,
                      template_name='users/singup.html',
                      context={'form': form}
                      )
    return render(request, template_name='users/singup.html')

@login_required
def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UpdateUser(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data['website']
            profile.biography = data['biography']
            profile.phone_number = data['phone_number']
            if data['picture']:
                profile.profile_picture = data['picture']

            profile.save()
            url = reverse('users:detail', kwargs={'username': request.user.username})
            return redirect(url)
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

DEPRECATED
"""

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

class SingupView(FormView):
    # Sing up view
    template_name = "users/singup.html"
    form_class = SingupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Save form data
        form.save()
        return super().form_valid(form)

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