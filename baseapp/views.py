from django.shortcuts import render

# Create your views here.

def user_profile(request, user_username):
    if request.method == "GET":
        return render(request, 'baseapp/user_profile.html')

def create_new(request):
    if request.method == "GET":
        return render(request, 'baseapp/create_post.html')