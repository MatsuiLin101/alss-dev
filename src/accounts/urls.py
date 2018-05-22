from django.conf.urls import url, include
from .views import (
    login_view,
    logout_view,
    register_view,
    forget_password_view,
    reset_password_view,
    edit_info_view,
    user_activate,
    resend_mail_view,
    reset_email_view
)

urlpatterns = [
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^forget-password/', forget_password_view, name='forget-password'),
    url(r'^edit-info/', edit_info_view, name='edit-info'),
    url(r'^resend-mail/', resend_mail_view, name='resend-mail'),
    url(r'^reset-password/(?P<key>[a-z0-9].*)/$', reset_password_view, name='reset-password'),
    url(r'^reset-email/(?P<key>[a-z0-9].*)/$', reset_email_view, name='reset-email'),
    url(r'^activate/(?P<key>[a-z0-9].*)/$', user_activate, name='activate'),
]
