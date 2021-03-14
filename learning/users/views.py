# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Forms
from users.forms import UpdateUser, SingupForm


# Create your views here.


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
            return redirect('feed')
        else:
            # Return to an 'invalid login' error message
            return render(request, 'users/login.html', context={'error': 'Invalid user or password'})
    #    import pdb
    #    pdb.set_trace()
    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def singup_view(request):
    if request.method == 'POST':

        form = SingupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

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
