"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter

from django.conf.urls import url, include
from . import views

app_name = 'api'


message_list = views.MessageViewset.as_view({
    'get': 'list'
})
message_detail = views.MessageViewset.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'process_new_post/$', views.ProcessNewSpotted.as_view(), name='process_new_post'),
    url(r'process_approved/$', views.ApprovedSpotted.as_view(), name='process_approved'),
    url(r'process_rejected/$', views.RejectedSpotted.as_view(), name='process_rejected'),
    url(r'process_deleted/$', views.DeletedSpotted.as_view(), name='process_deleted'),
    url(r'reject_options/$', views.RejectOptions.as_view(), name='reject_options'),
    url(r'my_options/$', views.MyDeleteOptions.as_view(), name='my_delete_options'),
    url(r'forme_options/$', views.ForMeDeleteOptions.as_view(), name='forme_delete_options'),

    url(r'list_approved/$', views.ApprovedList.as_view(), name='list_approved'),
    url(r'list_rejected/$', views.RejectedList.as_view(), name='list_rejected'),

    url(r'harumi/$', views.HarumiEndpoint.as_view(), name='harumi'),

    url(r'chatbot/process_chat_message/$', views.ProcessChatMessage.as_view(), name='process_chat_message'),
    url(r'chatbot/chat_submit/$', views.ChatSubmit.as_view(), name='chat_submit'),
    url(r'chatbot/chats/$', views.ChatListView.as_view(), name='chat-list'),
    url(r'chatbot/chats/(?P<pk>[0-9]+)/$', views.ChatDetailView.as_view(), name='chat-detail'),
    url(r'chatbot/messages/$', message_list, name='message-list'),
    url(r'chatbot/messages/(?P<pk>[0-9]+)/$', message_detail, name='message-detail'),

    url(r'get_coinhive_stats/$', views.CoinhiveStats.as_view(), name='coinhivestats'),
]

# urlpatterns += router.urls
