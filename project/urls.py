from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as rest_views
from django.contrib import admin
from django.contrib.auth.views import password_change, password_change_done
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^get-token/', rest_views.obtain_auth_token),  # pass username and password as POST fields

    url(r'^api/', include('api.urls', namespace='api')),

    url(r'change_password/$', password_change, {'template_name': 'rest_framework/change_password.html'}),
    url(r'change_password_done/$', password_change_done, {'template_name': 'rest_framework/change_password_done.html'}, name='password_change_done')
]

urlpatterns = format_suffix_patterns(urlpatterns)
