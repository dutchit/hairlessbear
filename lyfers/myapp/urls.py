from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views

urlpatterns = [
    url(r'^api/userprofiles/$', views.userprofile_list),
    url(r'^api/userprofile/(?P<pk>[0-9]+)/$', views.userprofile_detail),
    url(r'^api/providerprofiles/$', views.providerprofile_list),
    url(r'^api/jobs/$', views.jobs_list),
    url(r'^api/jobs/(?P<pk>[0-9]+)/$', views.user_jobs_list),
    url(r'^api/jobs/(?P<pk>[0-9]+)/(?P<job_number>[0-9]+)/$', views.user_job_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)