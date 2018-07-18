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
from relation.models import *
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.utils.html import escape, _js_escapes, normalize_newlines

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

