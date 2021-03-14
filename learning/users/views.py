# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Forms
from users.forms import UpdateUser

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
            return render(request, 'users/login.html', context={'error':'Invalid user or password'})
#    import pdb
#    pdb.set_trace()
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

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
            return render(request, 'users/singup.html', context={'error': 'Passwords do not match'})

        # Validate Username is not already taken
        if User.objects.filter(username=username):
            return render(request, 'users/singup.html', context={'error': 'Username is already taken'})

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