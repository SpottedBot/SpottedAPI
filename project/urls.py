from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views
from app import views
from django.contrib import admin
admin.autodiscover()

import app.views

# Examples:
# url(r'^$', 'project.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^get-token/', rest_views.obtain_auth_token),  # pass username and password as POST fields
    url(r'^spam-list/', views.SpamList.as_view()),
    url(r'^not-spam-list/', views.NotSpamList.as_view()),
    url(r'^predict/', views.EvalMessage.as_view()),
    url(r'^submit-data/', views.SubmitData.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)