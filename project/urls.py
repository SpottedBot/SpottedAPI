from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^get-token/', rest_views.obtain_auth_token),  # pass username and password as POST fields

    url(r'^api/', include('api.urls', namespace='api')),

]

urlpatterns = format_suffix_patterns(urlpatterns)
