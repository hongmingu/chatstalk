from django.shortcuts import render, redirect, reverse
from .forms import PostCreateForm
from relation.models import *
from object.models import *
from object.numbers import *
import uuid

from django.utils.timezone import now, timedelta

# Create your views here.

def user_profile(request, user_username):
    if request.method == "GET":
        user = None
        try:
            user = User.objects.get(userusername__username=user_username)
        except:
            return render(request, '404.html')
        if user is not None:
            following = None
            if Following.objects.filter(user=request.user, following=user).exists():
                following = True

            return render(request, 'baseapp/user_profile.html', {'chosen_user': user, 'following': following})

def create_new(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            title = None
            description = None
            has_another_profile = False

            if form.cleaned_data['whose'] == 'other':
                has_another_profile = True
            if form.cleaned_data['title'] == 'on':
                title = form.cleaned_data['title_content']
            if form.cleaned_data['description'] == 'on':
                description = form.cleaned_data['description_content']
            uuid_made = uuid.uuid4().hex
            post = Post.objects.create(user=request.user,
                                       title=title,
                                       description=description,
                                       has_another_profile=has_another_profile,
                                       uuid=uuid_made,
                                       is_open=False)
            if has_another_profile:
                PostProfile.objects.create(post=post, name=form.cleaned_data['name'])
            post_first_check = PostFirstCheck.objects.create(post=post)
            post_like_count = PostLikeCount.objects.create(post=post)
            post_comment_count = PostCommentCount.objects.create(post=post)
            post_chat = PostChat.objects.create(post=post, before=None, kind=POSTCHAT_START, uuid=uuid.uuid4().hex)
            # 여기서 post unique constraint 처리 해주면 좋긴 하나 지금 하기엔 하고 싶지 않다.
            return redirect(reverse('baseapp:post_update', kwargs={'uuid': uuid_made}))
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect(reverse('baseapp:main_create_log_in'))
        form = PostCreateForm
        return render(request, 'baseapp/create_new_first.html', {'form': form})


def post_update(request, uuid):
    if request.method == "GET":
        if request.user.is_authenticated:
            post = None
            try:
                post = Post.objects.get(uuid=uuid, user=request.user)

            except Post.DoesNotExist:
                return render(request, '404.html')
            just_created = {}
            if not post.postfirstcheck.first_checked:
                just_created['ok'] = 'on'
                post_first_check = post.postfirstcheck
                post_first_check.first_checked = True
                post_first_check.save()
            else:
                just_created['ok'] = 'off'
                if post.is_open:
                    just_created['current'] = 'open'
                else:
                    just_created['current'] = 'close'

            return render(request, 'baseapp/post_update.html', {'post': post, 'just_created': just_created})

def post(request, user_username, uuid):
    if request.method == "GET":

        return render(request, 'baseapp/post.html', )