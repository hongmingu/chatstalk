from django.shortcuts import render
from .forms import PostCreateForm
from object.models import *
from object.numbers import *


# Create your views here.

def user_profile(request, user_username):
    if request.method == "GET":
        return render(request, 'baseapp/user_profile.html')

def create_new(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            has_title = False
            has_description = False
            has_another_profile = False

            if form.cleaned_data['whose'] == 'other':
                has_another_profile = True
            if form.cleaned_data['title'] == 'on':
                has_title = True
            if form.cleaned_data['description'] == 'on':
                has_description = True
            post = Post.objects.create(user=request.user,
                                       has_title=has_title,
                                       has_description=has_description,
                                       has_another_profile=has_another_profile,
                                       uuid=uuid.uuid4().hex)
            if has_title:
                PostTitle.objects.create(post=post, title=form.cleaned_data['title_content'])
            if has_description:
                PostDescription.objects.create(post=post, description=form.cleaned_data['description_content'])
            if has_another_profile:
                PostProfile.objects.create(post=post, name=form.cleaned_data['name'])
            post_chat = PostChat.objects.create(post=post, before=None, kind=POSTCHAT_START)
            # 여기서 post unique constraint 처리 해주면 좋긴 하나 지금 하기엔 하고 싶지 않다.
            return render(request, 'baseapp/create_new_second.html', {'form': form, 'post': post})
    if request.method == "GET":
        form = PostCreateForm
        return render(request, 'baseapp/create_new_first.html', {'form': form})

def post(request, user_username, uuid):
    if request.method == "GET":

        return render(request, 'baseapp/post.html', )