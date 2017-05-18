from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.add_user),
    url(r'sendemail/$', views.send_email),
    url(r'inbox/(?P<pagenum>\d{1})/$', views.inbox),
    url(r'sentmails/(?P<pagenum>\d{1})/$', views.sent_mails),
    url(r'create_default_data/$', views.create_default_data),
    url(r'get_thread/(?P<id>\d{1})/', views.get_thread),
]