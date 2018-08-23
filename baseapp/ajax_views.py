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
                    post = Post.objects.get(uuid=request.POST['post_id'])
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


# 이건 포스트의 프로필 이미지를 지우기 위함.
@ensure_csrf_cookie
def re_create_new_remove_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                if request.POST.get('command', None) == 'remove_photo':
                    post_id = request.POST.get('post_id', None)
                    try:
                        post = Post.objects.get(pk=post_id)
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
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                print('got post: ' + str(post))

                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()
                    print('any made post chat?: ' + str(post_chat_last.pk))

                except PostChat.DoesNotExist:
                    print('has error on getting post_chat_last')
                print('has no error on getting post_chat_last')
                you_say = False
                if request.POST.get('you_say', None) == 'you':
                    you_say = True
                print(request.POST.get('text', None))
                post_chat = PostChat.objects.create(post=post, kind=POSTCHAT_TEXT, before=post_chat_last,
                                                    you_say=you_say, uuid=uuid.uuid4().hex)
                post_chat_text = PostChatText.objects.create(post_chat=post_chat, text=request.POST.get('text', None))
                return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})


'''

@ensure_csrf_cookie
def re_create_new_text(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                except:
                    return JsonResponse({'res': 0})
                print('got post: ' + str(post))
                try:
                    post_chat_create = PostChat.objects.create(post=post, kind=POSTCHAT_TEXT, before=None, you_say=True, uuid=uuid.uuid4().hex)
                    print('post chat has been created')
                except Exception as e:
                    print('if it has exception: ' + str(e))
                print('just created post chat: ' + str(post_chat_create.pk))

                try:
                    post_chat_last = PostChat.objects.last()
                    print('any made post chat?: ' + str(post_chat_last.pk))

                except PostChat.DoesNotExist:
                    print('has error on getting post_chat_last')
                print('has no error on getting post_chat_last')
                you_say = False
                if request.POST.get('you_say', None) == 'you':
                    you_say = True
                print(request.POST.get('text', None))
                post_chat = PostChat.objects.create(kind=POSTCHAT_TEXT, before=post_chat_last, you_say=you_say, uuid=uuid.uuid4().hex)
                post_chat_text = PostChatText.objects.create(post_chat=post_chat, text=request.POST.get('text', None))
                return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})'''


# 2018-07-28 해야 할 일: postchatphoto 업로드 테스트.


@ensure_csrf_cookie
def re_create_new_chat_photo(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST['post_id']
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_chat_last = PostChat.objects.filter(post=post).last()
                except PostChat.DoesNotExist:
                    return JsonResponse({'res': 0})
                form = PostChatPhotoForm(request.POST, request.FILES)
                if form.is_valid():
                    you_say = True
                    if request.POST.get('you_say', None) == 'someone':
                        you_say = False
                    post_chat = PostChat.objects.create(kind=POSTCHAT_PHOTO, post=post, before=post_chat_last,
                                                        you_say=you_say, uuid=uuid.uuid4().hex)
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
                    return JsonResponse({'res': 1, 'content': post_chat.get_value()})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_update(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                # 여기서 None 이 나오진 않고 기껏해야 빈 문자열이 오는 것이다.
                open = request.POST.get('open', None)
                title_command = request.POST.get('title_command', None)
                desc_command = request.POST.get('desc_command', None)
                print(title_command)
                print(desc_command)
                if open == 'open':
                    post.is_open = True
                elif open == 'close':
                    post.is_open = False
                if title_command == 'removed':
                    post.title = None
                elif title_command == 'add':
                    post.title = request.POST.get('title', None)
                if desc_command == 'removed':
                    post.description = None
                elif desc_command == 'add':
                    post.description = request.POST.get('description', None)

                post.save()
                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_remove(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_chat_id = request.POST.get('post_chat_id', None)
                try:
                    post_chat = PostChat.objects.get(uuid=post_chat_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat.delete()
                return JsonResponse({'res': 1})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_modify_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                print(post_id)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                post_chat_set = post.postchat_set.all().order_by('-created')[:10]
                from django.core import serializers
                post_chat_set = serializers.serialize('python', post_chat_set)
                actual_data = [PostChat.objects.get(pk=item['pk']).get_value() for item in post_chat_set]
                output = json.dumps(actual_data)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_chat_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                post_chat_id = request.POST.get('post_chat_id', None)
                print(post_id)
                print(post_chat_id)
                try:
                    post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                from django.db.models import Q
                standard_post_chat = PostChat.objects.get(uuid=post_chat_id)
                post_chat_set = PostChat.objects.filter(
                    Q(post=post) & Q(created__lt=standard_post_chat.created)).order_by('-created')[:10]
                from django.core import serializers
                post_chat_set = serializers.serialize('python', post_chat_set)
                actual_data = [PostChat.objects.get(pk=item['pk']).get_value() for item in post_chat_set]
                output = json.dumps(actual_data)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_comment_add(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                text = request.POST.get('comment', None)
                try:
                    # post = Post.objects.get(uuid=post_id)
                    post = Post.objects.last()

                except:
                    return JsonResponse({'res': 0})
                try:
                    with transaction.atomic():
                        post_comment = PostComment.objects.create(post=post, user=request.user, uuid=uuid.uuid4().hex,
                                                                  text=text)
                        from django.db.models import F
                        post_comment_count = post.postcommentcount
                        post_comment_count.count = F('count') + 1
                        post_comment_count.save()
                        # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                except Exception:
                    return JsonResponse({'res': 0})

                output = []
                sub_output = {}
                if post_comment is not None:
                    sub_output = {
                            'comment_user_id': post_comment.user.username,
                            'comment_username': post_comment.user.userusername.username,
                            'comment_text': post_comment.text,
                            'comment_created': post_comment.created,
                            'comment_uuid': post_comment.uuid,
                        }
                output.append(sub_output)
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_comment_delete(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                comment_id = request.POST.get('comment_id', None)
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                    # post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                try:
                    comment = PostComment.objects.get(uuid=comment_id, user=request.user)
                except:
                    try:
                        comment = PostComment.objects.get(uuid=comment_id, post=post, post__user=request.user)
                    except:
                        return JsonResponse({'res': 0})

                try:
                    with transaction.atomic():
                        comment.delete()
                        from django.db.models import F
                        post_comment_count = post.postcommentcount
                        post_comment_count.count = F('count') - 1
                        post_comment_count.save()
                except Exception:
                    return JsonResponse({'res': 0})
                return JsonResponse({'res': 1})
        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_comment_more_load(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                last_comment_id = request.POST.get('last_comment_id', None)

                try:
                    post = Post.objects.last()
                    # post = Post.objects.get(uuid=post_id)
                except Exception:
                    return JsonResponse({'res': 0})

                post_comment_last = PostComment.objects.get(uuid=last_comment_id)

                post_comments = PostComment.objects.filter(Q(post=post) & Q(created__gt=post_comment_last.created)).order_by('created')[:20]

                post_comment_uuids = [post_comment.uuid for post_comment in post_comments]
                output = []

                post_comment_end = PostComment.objects.last()

                end = False
                if post_comments:
                    for item in post_comment_uuids:
                        try:
                            post_comment = PostComment.objects.get(uuid=item)
                        except:
                            pass
                        if post_comment is not None:
                            sub_output = {
                                'comment_user_id': post_comment.user.username,
                                'comment_username': post_comment.user.userusername.username,
                                'comment_text': post_comment.text,
                                'comment_created': post_comment.created,
                                'comment_uuid': post_comment.uuid,
                            }
                            output.append(sub_output)
                            if post_comment.uuid == post_comment_end.uuid:
                                end = True
                else:
                    output = None
                    end = True

                return JsonResponse({'res': 1, 'set': output, 'end': end})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_post_like(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                    # post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})
                try:
                    post_like = PostLike.objects.get(post=post, user=request.user)
                except PostLike.DoesNotExist:
                    post_like = None

                liked = None
                if post_like is not None:
                    try:
                        with transaction.atomic():
                            post_like.delete()
                            from django.db.models import F
                            post_like_count = post.postlikecount
                            post_like_count.count = F('count') - 1
                            post_like_count.save()
                            liked = False
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})
                else:
                    try:
                        with transaction.atomic():
                            post_like = PostLike.objects.create(post=post, user=request.user)
                            from django.db.models import F
                            post_like_count = post.postlikecount
                            post_like_count.count = F('count') + 1
                            post_like_count.save()
                            liked = True
                            # customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
                    except Exception:
                        return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'liked': liked})

        return JsonResponse({'res': 2})

@ensure_csrf_cookie
def re_user_home_populate(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                except:
                    return JsonResponse({'res': 0})
                print(post.pk)
                from django.db.models import Q
                name = post.user.usertextname.name
                profile_photo = post.user.userphoto.file_50_url()

                if post.has_another_profile:
                    name = post.postprofile.name
                    profile_photo = post.postprofile.file_50_url()
                print(post.get_three_comments())
                you_liked = False
                if PostLike.objects.filter(user=request.user, post=post).exists():
                    you_liked = True
                post_chat_read = PostChatRead.objects.filter(post=post, user=request.user).last()
                post_chat = None
                post_chat_last_chat = None
                if post_chat_read is None:
                    try:
                        post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                    except IndexError:
                        post_chat_last_chat = {'kind': 'start'}
                    if post_chat is not None:
                        if post_chat.kind == POSTCHAT_TEXT:
                            post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                    'text': escape(post_chat.postchattext.text)}
                        elif post_chat.kind == POSTCHAT_PHOTO:
                            post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}
                else:
                    if post_chat_read.post_chat.kind == POSTCHAT_START:
                        try:
                            post_chat = PostChat.objects.filter(post=post).order_by('created')[1]
                        except IndexError:
                            post_chat_last_chat = {'kind': 'start'}
                        if post_chat is not None:
                            if post_chat.kind == POSTCHAT_TEXT:
                                post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say,
                                                  'text': escape(post_chat.postchattext.text)}
                            elif post_chat.kind == POSTCHAT_PHOTO:
                                post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say,
                                                  'url': post_chat.postchatphoto.file.url}
                    elif post_chat_read.post_chat.kind == POSTCHAT_TEXT:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'text', 'you_say': post_chat.you_say, 'text': escape(post_chat.postchattext.text)}
                    elif post_chat_read.post_chat.kind == POSTCHAT_PHOTO:
                        post_chat = post_chat_read.post_chat
                        post_chat_last_chat = {'kind': 'photo', 'you_say': post_chat.you_say, 'url': post_chat.postchatphoto.file.url}

                new = True
                post_chat_last = PostChat.objects.filter(post=post).last()
                post_chat_read_last = PostChatRead.objects.filter(post=post, user=request.user).last()

                if post_chat_read_last is not None:
                    if post_chat_read_last.post_chat == post_chat_last:
                        new = False
                    else:
                        new = True

                output = {'title': post.title,
                          'desc': post.description,
                          'username': post.user.userusername.username,
                          'name': name,
                          'photo': profile_photo,
                          'created': post.created,
                          'last_chat': post_chat_last_chat,
                          'absolute_url': post.get_absolute_url(),
                          'id': post.uuid,
                          'like_count': post.postlikecount.count,
                          'you_liked': you_liked,
                          'comment_count': post.postcommentcount.count,
                          'three_comments': post.get_three_comments(),
                          'new': new,
                          }
                return JsonResponse({'res': 1, 'set': output})

        return JsonResponse({'res': 2})


@ensure_csrf_cookie
def re_post_read(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post_id = request.POST.get('post_id', None)
                try:
                    post = Post.objects.last()
                    # post = Post.objects.get(uuid=post_id)
                except:
                    return JsonResponse({'res': 0})

                return JsonResponse({'res': 1, 'set': {'id': 'hohohohoho'}})

        return JsonResponse({'res': 2})