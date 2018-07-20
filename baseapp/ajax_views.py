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

@ensure_csrf_cookie
def create_new(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                if request.POST.get('whose', None) == 'self':
                    new_post = Post.objects.create()
                    # 우선 만들되 비공개로 한다. 그러면 현재 만들어져있지만 비공개인 상태.
                    # 이 상황에선 POSTCHAT_START랑 POSTCHAT_REST가 만들어져 있는 상태여야 한다. 에러를 막기 위해서.
                    # 그 다음 칸에서 프로필사진, 첫 문장들 설정.
                    # 여기서 첫 문장이 특별한게 없으면 REST가 정해져 있는 그대로 진행된다. 여기서 첫 문장이 있는 경우에만
                    # 바로 REST 가 삭제된다. 삭제하는 게 낫다. 그냥 삭제해. REST를 따로 표시할 때 여기에 REST가 몇개나 있는지
                    # 그런것도 판단하기엔 무리가 있다. 그러므로 REST를 삭제하라. 괜히 0개인 REST가 존재해서 귀찮아질 필요가 없다. 

                    pass
                elif request.POST.get('whose', None) == 'other':
                    pass


        return JsonResponse({'res': 2})
