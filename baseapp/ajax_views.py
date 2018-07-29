import json
import urllib
from urllib.parse import urlparse

from PIL import Image
from io import BytesIO
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now, timedelta
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from authapp import options
from authapp import texts
from object.models import *
from .forms import PostProfilePhotoForm, PostChatPhotoForm
from relation.models import *
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.utils.html import escape, _js_escapes, normalize_newlines
from object.numbers import *


# Create your models here.
# 좋아요 비공개 할 수 있게
# 챗스톡, 페이지픽, 임플린, 챗카부 순으로 만들자.

@ensure_csrf_cookie
def task(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():

                if request.POST.get('command', None) is None:
                    return JsonResponse({'res': 2})

                elif request.POST.get('command', None) == 'home':
                    if request.POST.get('last_num', None) == '':
                        Post.objects.all()
                    else:
                        print(request.POST.get('last_num', None))

                    return JsonResponse({'res': 1})
                elif request.POST.get('command', None) == '_home':
                    post = None
                    try:
                        post = Post.objects.get(pk=request.POST.get('pk', None))
                    except Post.DoesNotExist:
                        post = Post.objects.all().values('pk')
                        print(post)
                        return JsonResponse({'res': 0, 'error': 0})

                    content = {}
                    content['username'] = post.user.userusername.username
                    if post.has_title:
                        content['title'] = post.posttitle.title
                    if post.has_description:
                        content['description'] = post.postdescription.description
                    content['like_count'] = post.postlikecount.count

                    return JsonResponse({'res': 1, 'message': content})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_create_new_upload_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            if request.is_ajax():
                try:
                    post = Post.objects.get(pk=request.POST['post_num'])
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_profile = PostProfile.objects.get(post=post)
                except:
                    return JsonResponse({'res': 0})
                form = PostProfilePhotoForm(request.POST, request.FILES, instance=post_profile)
                if form.is_valid():

                    DJANGO_TYPE = request.FILES['file'].content_type

                    if DJANGO_TYPE == 'image/jpeg':
                        PIL_TYPE = 'jpeg'
                        FILE_EXTENSION = 'jpg'
                    elif DJANGO_TYPE == 'image/png':
                        PIL_TYPE = 'png'
                        FILE_EXTENSION = 'png'
                        # DJANGO_TYPE == 'image/gif
                    else:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

                    from io import BytesIO
                    from PIL import Image
                    from django.core.files.uploadedfile import SimpleUploadedFile
                    import os
                    x = float(request.POST['x'])
                    y = float(request.POST['y'])
                    width = float(request.POST['width'])
                    height = float(request.POST['height'])
                    rotate = float(request.POST['rotate'])
                    # Open original photo which we want to thumbnail using PIL's Image
                    try:
                        with transaction.atomic():

                            image = Image.open(BytesIO(request.FILES['file'].read()))
                            image_modified = image.rotate(-1 * rotate, expand=True).crop((x, y, x + width, y + height))
                            # use our PIL Image object to create the thumbnail, which already
                            image = image_modified.resize((300, 300), Image.ANTIALIAS)

                            # Save the thumbnail
                            temp_handle = BytesIO()
                            image.save(temp_handle, PIL_TYPE, quality=90)
                            temp_handle.seek(0)

                            # Save image to a SimpleUploadedFile which can be saved into ImageField
                            # print(os.path.split(request.FILES['file'].name)[-1])
                            suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                                     temp_handle.read(), content_type=DJANGO_TYPE)
                            # Save SimpleUploadedFile into image field
                            post_profile.file_300.save(
                                '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                                suf, save=True)

                            # request.FILES['file'].seek(0)
                            # image = Image.open(BytesIO(request.FILES['file'].read()))

                            # use our PIL Image object to create the thumbnail, which already
                            image = image_modified.resize((50, 50), Image.ANTIALIAS)

                            # Save the thumbnail
                            temp_handle = BytesIO()
                            image.save(temp_handle, PIL_TYPE, quality=90)
                            temp_handle.seek(0)

                            # Save image to a SimpleUploadedFile which can be saved into ImageField
                            # print(os.path.split(request.FILES['file'].name)[-1])
                            suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                                     temp_handle.read(), content_type=DJANGO_TYPE)
                            # Save SimpleUploadedFile into image field
                            # print(os.path.splitext(suf.name)[0])
                            # user_photo.file_50.save(
                            #     '50_%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                            #     suf, save=True)
                            post_profile.file_50.save(
                                '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                                suf, save=True)
                            return JsonResponse({'res': 1, 'url': post_profile.file_300.url})
                    except Exception:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

            return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})




@ensure_csrf_cookie
def re_create_new_remove_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                if request.POST.get('command', None) == 'remove_photo':
                    post_num = request.POST.get('post_num', None)
                    try:
                        post = Post.objects.get(pk=post_num)
                    except:
                        return JsonResponse({'res': 0})
                    try:
                        post_profile = PostProfile.objects.get(post=post)
                    except:
                        return JsonResponse({'res': 0})
                    post_profile.file_50 = None
                    post_profile.file_300 = None
                    post_profile.save()
                    return JsonResponse({'res': 1})
                elif request.POST.get('whose', None) == 'other':
                    pass


        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_create_new_text(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_pk = request.POST.get('post_pk', None)
                try:
                    post = Post.objects.get(pk=post_pk)
                except:
                    return JsonResponse({'res': 0})
                post_chat_last = None
                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()
                except PostChat.DoesNotExist:
                    return JsonResponse({'res': 0})
                post_chat = PostChat.objects.create(kind=POSTCHAT_TEXT, before=post_chat_last)
                post_chat_text = PostChatText.objects.create(post_chat=post_chat, text=request.POST.get('text', None))
                return JsonResponse({'res': 1, 'text': post_chat.get_value()})

        return JsonResponse({'res': 2})

# 2018-07-28 해야 할 일: postchatphoto 업로드 테스트.


@ensure_csrf_cookie
def re_create_new_chat_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_pk = request.POST['post_pk']
                try:
                    post = Post.objects.get(pk=post_pk)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()
                except PostChat.DoesNotExist:
                    return JsonResponse({'res': 0})
                form = PostChatPhotoForm(request.POST, request.FILES)
                if form.is_valid():
                    post_chat = PostChat.objects.create(kind=POSTCHAT_PHOTO, post=post, before=post_chat_last)
                    post_chat_photo = PostChatPhoto.objects.create(post_chat=post_chat)

                    DJANGO_TYPE = request.FILES['file'].content_type

                    if DJANGO_TYPE == 'image/jpeg':
                        PIL_TYPE = 'jpeg'
                        FILE_EXTENSION = 'jpg'
                    elif DJANGO_TYPE == 'image/png':
                        PIL_TYPE = 'png'
                        FILE_EXTENSION = 'png'
                        # DJANGO_TYPE == 'image/gif
                    else:
                        return JsonResponse({'res': 0, 'message': texts.UNEXPECTED_ERROR})

                    from io import BytesIO
                    from PIL import Image
                    from django.core.files.uploadedfile import SimpleUploadedFile
                    import os
                    rotate = float(request.POST['rotate'])
                    # Open original photo which we want to thumbnail using PIL's Image

                    image = Image.open(BytesIO(request.FILES['file'].read()))
                    image = image.rotate(-1 * rotate, expand=True)
                    # use our PIL Image object to create the thumbnail, which already
                    # Save the thumbnail
                    temp_handle = BytesIO()
                    image.save(temp_handle, PIL_TYPE, quality=70)
                    temp_handle.seek(0)

                    # Save image to a SimpleUploadedFile which can be saved into ImageField
                    # print(os.path.split(request.FILES['file'].name)[-1])
                    suf = SimpleUploadedFile(os.path.split(request.FILES['file'].name)[-1],
                                             temp_handle.read(), content_type=DJANGO_TYPE)
                    # Save SimpleUploadedFile into image field
                    post_chat_photo.file.save(
                        '%s.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
                        suf, save=True)

                    # request.FILES['file'].seek(0)
                    # image = Image.open(BytesIO(request.FILES['file'].read()))

                    # use our PIL Image object to create the thumbnail, which already
                    return JsonResponse({'res': 1, 'url': post_chat_photo.file.url})

        return JsonResponse({'res': 2})
