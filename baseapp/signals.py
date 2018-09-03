from django.db.models.signals import post_save
from django.dispatch import receiver
from object.models import *


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


