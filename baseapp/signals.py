from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from object.models import *
from relation.models import *
from notice.models import *
from django.db import transaction
from django.db.models import F

from object.numbers import *
KINDS_CHOICES = (
    (POSTCHAT_START, "start"),
    (POSTCHAT_TEXT, "text"),
    (POSTCHAT_PHOTO, "photo"),
)


@receiver(post_save, sender=PostChat)
def created_post_chat(sender, instance, created, **kwargs):
    if created:
        if instance.kind != POSTCHAT_START:
            PostChatLikeCount.objects.create(post_chat=instance)
        PostChatRestMessageCount.objects.create(post_chat=instance)


@receiver(post_save, sender=PostChatRestMessage)
def created_post_rest_message(sender, instance, created, **kwargs):
    if created:
        PostChatRestMessageLikeCount.objects.create(post_chat_rest_message=instance)


# notice follow

@receiver(post_save, sender=Follow)
def created_follow(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.follow)
                notice_follow = NoticeFollow.objects.create(notice=notice, follow=instance)
                notice_count = instance.follow.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticeFollow)#이걸 pre_delete로 해야하나?
def deleted_notice_follow(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_follow


@receiver(post_save, sender=PostFollow)
def created_post_follow(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.post.user)
                notice_post_follow = NoticePostFollow.objects.create(notice=notice, post_follow=instance)
                notice_count = instance.post.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostFollow)#이걸 pre_delete로 해야하나?
def deleted_notice_post_follow(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_comment
@receiver(post_save, sender=PostComment)
def created_post_comment(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.post.user)
                notice_post_comment = NoticePostComment.objects.create(notice=notice, post_comment=instance)
                notice_count = instance.post.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostComment)#이걸 pre_delete로 해야하나?
def deleted_notice_post_comment(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_like
@receiver(post_save, sender=PostLike)
def created_post_like(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.follow)
                notice_post_like = NoticePostLike.objects.create(notice=notice, post_like=instance)
                notice_count = instance.post.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_like(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_chat_like
@receiver(post_save, sender=PostChatLike)
def created_post_chat_like(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.follow)
                notice_post_chat_like = NoticePostChatLike.objects.create(notice=notice, post_chat_like=instance)
                notice_count = instance.postchat.post.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostChatLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_like(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_chat_rest
@receiver(post_save, sender=PostChatRestMessage)
def created_post_chat_rest(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.follow)
                notice_post_chat_rest = NoticePostChatRest.objects.create(notice=notice, post_chat_rest=instance)
                notice_count = instance.user.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostChatRest)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_rest(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass


# notice post_chat_rest_like
@receiver(post_save, sender=PostChatRestMessageLike)
def created_post_chat_rest_like(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                notice = Notice.objects.create(user=instance.follow)
                notice_post_chat_rest_like = NoticePostChatRestLike.objects.create(notice=notice, post_chat_rest_like=instance)
                notice_count = instance.follow.noticecount
                notice_count.count = F('count') + 1
                notice_count.save()
        except Exception:
            pass


@receiver(post_delete, sender=NoticePostChatRestLike)#이걸 pre_delete로 해야하나?
def deleted_notice_post_chat_rest_like(sender, instance, **kwargs):
    try:
        if instance.notice:
            try:
                with transaction.atomic():
                    if instance.notice.checked is False:
                        notice_count = instance.notice.user.noticecount
                        notice_count.count = F('count') - 1
                        notice_count.save()
                    instance.notice.delete()
            except Exception:
                pass
    except:
        pass

