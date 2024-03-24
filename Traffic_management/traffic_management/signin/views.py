from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import os
# from django.core.mail import send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from .models import ActivationToken
# import secrets
# import string

# Create your views here.
def home(request):
    return HttpResponse("Hello home")

def errorpage(request):
    return HttpResponse("Bad Credentials")

# Addtion of email authentication and activation
# def generate_activation_token(length=32):
#     alphabet = string.ascii_letters + string.digits
#     token = ''.join(secrets.choice(alphabet) for _ in range(length))
#     return token

# def send_activation_email(request, user):
#     token = generate_activation_token()
#     ActivationToken.objects.create(user=user, token=token)
#     current_site = get_current_site(request)
#     subject = 'Activate Your Account'
#     message = render_to_string('yourapp/account_activation_email.html', {
#         'user': user,
#         'domain': current_site.domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': token,
#     })
#     user.email_user(subject, message)

def signin(request):
    if request.method == "POST":
        name = request.POST['name']
        pass1 = request.POST['password']
        # print("got details")
        user = authenticate(username=name, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            # print("Bad ceds")
            messages.error(request, "Bad Credentials")
            # ask what to do here
            return redirect('errorpage')



    return render(request, 'signin/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        print("Your account has been successfully created")

        messages.success(request, "Your account has been successfully created")
        return redirect('signin')

    return render(request, 'signin/register.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('user')
    

def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')

def user_func(request):
    return render(request, "user/user.html")
    # return HttpResponse("user html")

def results_func(request):
    return HttpResponse("result html")

def upload_video(request):
    if request.method == 'POST' and request.FILES['video_file']:
        video_file = request.FILES['video_file']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        uploaded_file_url = fs.url(filename)
        print("Uploaded successfully")
        return redirect('/signin/results')
        # Do something with the uploaded file, e.g., save it to a model
        # return render(request, 'your_template.html', {
        #     'uploaded_file_url': uploaded_file_url
        # })
    return HttpResponse("Not uploaded")