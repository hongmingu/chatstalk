from django.urls import path, re_path
from authapp import views as authviews
from authapp import ajax_views as auth_ajax_views
from baseapp import ajax_views as base_ajax_views
from baseapp import views

app_name = 'baseapp'

urlpatterns = [

    re_path(r'^$', authviews.main_create_log_in, name='main_create_log_in'),
    re_path(r'^create/new/$', views.create_new, name='create_new'),
    re_path(r'^(?P<user_username>([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?))/$', views.user_profile, name='user_profile'),
    re_path(r'^(?P<user_username>([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?))/(?P<uuid>([0-9a-f]{32}))/$',
            views.post, name='post'),
    re_path(r'^post/update/(?P<uuid>([0-9a-f]{32}))/$', views.post_update, name='post_update'),

    re_path(r'^re_settings/ajax/$', auth_ajax_views.re_settings, name='re_settings'),
    re_path(r'^re_settings/ajax/upload_user_photo/$', auth_ajax_views.upload_user_photo, name='re_upload_user_photo'),
    re_path(r'^re/task/$', base_ajax_views.task, name='re_task'),
    # re_path(r'^re/create/new/$', base_ajax_views.re_create_new, name='re_create_new'),
    re_path(r'^re/create/new/upload_photo/$', base_ajax_views.re_create_new_upload_photo, name='re_create_new_upload_photo'),
    re_path(r'^re/create/new/remove_photo/$', base_ajax_views.re_create_new_remove_photo, name='re_create_new_remove_photo'),
    re_path(r'^re/create/new/text/$', base_ajax_views.re_create_new_text,
            name='re_create_new_text'),
    re_path(r'^re/create/new/chat_photo/$', base_ajax_views.re_create_new_chat_photo,
            name='re_create_new_chat_photo'),
    re_path(r'^re/post/update/$', base_ajax_views.re_post_update,
            name='re_post_update'),
    re_path(r'^re/post/chat/remove/$', base_ajax_views.re_post_chat_remove,
            name='re_post_chat_remove'),

    re_path(r'^re/post/chat/modify/populate/$', base_ajax_views.re_post_chat_modify_populate,
            name='re_post_chat_modify_populate'),
    re_path(r'^re/post/chat/more/load/$', base_ajax_views.re_post_chat_more_load,
            name='re_post_chat_more_load'),
    re_path(r'^re/user/home/populate/$', base_ajax_views.re_user_home_populate,
            name='re_user_home_populate'),
    re_path(r'^re/comment/add/$', base_ajax_views.re_comment_add,
            name='re_comment_add'),
    re_path(r'^re/comment/delete/$', base_ajax_views.re_comment_delete,
            name='re_comment_delete'),
    re_path(r'^re/comment/more/load/$', base_ajax_views.re_comment_more_load,
            name='re_comment_more_load'),
    re_path(r'^re/post/like/$', base_ajax_views.re_post_like,
            name='re_post_like'),

    re_path(r'^re/post/already/read/$', base_ajax_views.re_post_already_read,
            name='re_post_already_read'),
    # re_path(r'^email/key/send/$', views.email_key_send, name='email_key_send'),
    # re_path(r'^email/key/confirm/(?P<uid>([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?))/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        # views.email_key_confirm, name='email_key_confirm'),
    # re_path(r'^logout/$', views.log_out, name='log_out'),
    # re_path(r'^username/change/$', views.username_change, name='username_change'),
    # re_path(r'^password/change/$', views.password_change, name='password_change'),
    # re_path(r'^password/reset/$', views.password_reset, name='password_reset'),
    # re_path(r'^email/add/$', views.email_add, name='email_add'),
]
'''
    url(r'^create/$', views.main_create_log_in, name='create'),
'''