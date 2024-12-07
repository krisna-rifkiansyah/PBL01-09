import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserRegisterForm, PostForm
from .models import Post, User, LogEntry
from django.core.files.base import ContentFile
from .utils import verify_token, get_client_ip, create_log_entry, generate_token


def home(request):
    session = "GUEST" if request.user.is_anonymous else request.user.username
    ipaddr = get_client_ip(request)

    create_log_entry(
        key="HTTPAccess",
        txt=request.path,
        session=session,
        ipaddr=ipaddr
    )

    posts = Post.objects.all().order_by('-date_posted')
    for post in posts:
        post.user.token = generate_token(post.user.username)
    return render(request, 'myapp/home.html', {'posts': posts})

def profile_secure(request, token):
    session = "GUEST" if request.user.is_anonymous else request.user.username
    ipaddr = get_client_ip(request)

    create_log_entry(
        key="HTTPAccess",
        txt=request.path,
        session=session,
        ipaddr=ipaddr
    )

    username = verify_token(token)
    user = get_object_or_404(User, username=username)
    posts = user.post_set.all().order_by('-date_posted')
    return render(request, 'myapp/user_profile.html', {'user_profile': user, 'posts': posts})

def user_profile(request, username):
    session = "GUEST" if request.user.is_anonymous else request.user.username
    ipaddr = get_client_ip(request)

    create_log_entry(
        key="HTTPAccess",
        txt=request.path,
        session=session,
        ipaddr=ipaddr
    )

    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-date_posted')
    return render(request, 'myapp/user_profile.html', {'user_profile': user, 'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.warning(request, 'Password Must be 8 Letters or More')
    else:
        form = UserRegisterForm()
    
    return render(request, 'myapp/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if user.is_superuser or user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('profile')
        else:
            messages.warning(request, 'Login failed. Check your username and password.')
    elif 'next' in request.GET and not request.user.is_authenticated:
        messages.warning(request, 'You Need to Login First')
        
    return render(request, 'myapp/login.html')


@login_required
def profile(request):
    session = "GUEST" if request.user.is_anonymous else request.user.username
    ipaddr = get_client_ip(request)

    create_log_entry(
        key="HTTPAccess",
        txt=request.path,
        session=session,
        ipaddr=ipaddr
    )

    posts = Post.objects.filter(user=request.user).order_by('-date_posted')
    return render(request, 'myapp/profile.html', {'posts': posts})

@login_required
def post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        post = Post.objects.create(user=request.user, text=text, image=image)
        return redirect('profile')
    return render(request, 'myapp/post.html')

# @login_required
# def post(request):
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         image_file = request.FILES.get('image')

#         image_base64 = None
#         if image_file:
#             image_data = image_file.read()
#             image_base64 = base64.b64encode(image_data).decode('utf-8')

#         Post.objects.create(user=request.user, text=text, image_base64=image_base64)
#         return redirect('home')

#     return render(request, 'myapp/post.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    session = "GUEST" if request.user.is_anonymous else request.user.username
    ipaddr = get_client_ip(request)

    create_log_entry(
        key="HTTPAccess",
        txt=request.path,
        session=session,
        ipaddr=ipaddr
    )

    users = User.objects.all()
    posts = Post.objects.all().order_by('date_posted')
    return render(request, 'myapp/admin_dashboard.html', {'users': users, 'posts': posts})

def log_everything_view(request):
    if not request.user.is_staff:
        return render(request, 'error')

    logs = LogEntry.objects.all().order_by('-time')
    return render(request, 'log_everything.html', {'logs': logs})
